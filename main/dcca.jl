using DataFrames
using CSV
using Dates
using Statistics
using ShiftedArrays
using Polynomials
using StatsBase, Random
using CairoMakie
using Interpolations
using RollingFunctions
################################################################
#ci_keys is the parameter describing the length of the time series to study.
ci_keys = Int[250,500,1000,2000,4000,8000]
#ci-points describes the window sizes at whcih the critical values are given (in function of ci_keys).
ci_points = Int[4 ,8, 16, 32, 64, 128, 256]
# ci_values stocks the critical values describing the 95% confidence interval depending on the ci_keys parameter.
ci_values = [Float64[0.129, 0.156, 0.212, 0.305, 0.448], Float64[0.091, 0.109, 0.147, 0.210, 0.302, 0.447], Float64[0.064, 0.077, 0.104, 0.146, 0.208, 0.306, 0.449], Float64[0.045,0.054,0.073,0.102,0.145,0.209,0.304], Float64[0.032,0.039,0.052,0.072,0.102,0.145,0.209], Float64[0.023, 0.027, 0.037, 0.051, 0.072, 0.102, 0.146]]
function empirical_CI(data_length; start = 4, stop = div(data_length,10))
    if stop > 256 #256 is the biggest window size found in litterature about confidence intervals.
        @warn "`stop` parameter is greater what can be found in the litterature.\n For Every point past 256, the confidence interval is linearly extrapolated."
    end
    points = collect(start:stop)
    critical_values = complete_CI(data_length, points)
    return points, critical_values
end
function nearest_neighbour(value, listOfValues)
    index_nn = findmin(abs.(listOfValues .- value))[2] #index of the nearest neighbour
    nn = listOfValues[index_nn] #value of the nearest neighbour
    return nn, index_nn
end
function interpolate(x,y)
    interpolation_function = LinearInterpolation(x,y, extrapolation_bc = Line())
    return interpolation_function
end
function complete_CI(data_length, points)
    partial_CIs = ci_values[nearest_neighbour(data_length, ci_keys)[2]]
    total_CI = interpolate(ci_points[1:length(partial_CIs)], partial_CIs)(points)
    return round.(total_CI, digits = 3)
end
########################################################################
function DCCA_coefficient(data1::Array{Float64,1},data2::Array{Float64,1}; box_start = 3, box_stop = div(length(data1),10), nb_pts = 30, order = 1)
    if length(data1) != length(data2)
        error("the two data series must have same length.")
    end
    if box_stop > div(length(data1),10)
        @warn "`Box_stop` parameter greater that 1/10 of data length. Results at large time scales might not make sense."
    end
    x = log_space(box_start,box_stop,nb_pts)
    y = dcca_only(data1,data2; box_start = box_start, box_stop = box_stop, nb_pts = nb_pts, order = order)
    return x, y
end
function rhoDCCA(data1::Array{Float64,1},data2::Array{Float64,1}; box_start = 3, box_stop = div(length(data1),10), nb_pts = 30, order = 1)
    if length(data1) != length(data2)
        error("the two data series must have same length.")
    end
    if box_stop > div(length(data1),10)
        @warn "`Box_stop` parameter greater that 1/10 of data length. Results at large time scales might not make sense."
    end
    x = log_space(box_start,box_stop,nb_pts)
    y = dcca(data1,data2; box_start = box_start, box_stop = box_stop, nb_pts = nb_pts, order = order)
    return x, y
end
function log_space(start::Int,stop::Int,num::Int)
    spacing = map(x -> round(Int,x), exp10.(range(log10(start), stop=log10(stop), length=num)))
    return sort(unique(spacing))
end
function dcca_only(data1::Array{Float64,1},data2::Array{Float64,1};
    box_start::Int = 3, box_stop::Int = div(length(data1),10), nb_pts::Int = 30, order = 2)
    if box_start < 3
        print("ERROR : size of windows must be greater than 3")
        return
    end
    window_sizes = log_space(box_start,box_stop,nb_pts)
    rho_DCCA = zeros(length(window_sizes))
    ffi, ff1i, ff2i = 0, 0, 0
    for (index,i) in enumerate(window_sizes)
        xi = partitioning(integrate(data1),i)
        yi = partitioning(integrate(data2),i)
        n = size(xi,1)
        m = size(xi,2)
        for j in 1:n
            #testing another version of detrending
            if order == 1
                seg_x = detrending(xi[j,:])
                seg_y = detrending(yi[j,:])
            else
                seg_x = detrending_poly(xi[j,:], order)
                seg_y = detrending_poly(yi[j,:], order)
            end
            ffi += (1/n)*((1/i)*seg_x'seg_y)
            ff1i += (1/n)*((1/i)*seg_x'seg_x)
            ff2i += (1/n)*((1/i)*seg_y'seg_y)
        end
        rho_DCCA[index] = ffi
    end
    return  rho_DCCA
end
function dcca(data1::Array{Float64,1},data2::Array{Float64,1};
    box_start::Int = 3, box_stop::Int = div(length(data1),10), nb_pts::Int = 30, order = 2)
    if box_start < 3
        print("ERROR : size of windows must be greater than 3")
        return
    end
    window_sizes = log_space(box_start,box_stop,nb_pts)
    rho_DCCA = zeros(length(window_sizes))
    ffi, ff1i, ff2i = 0, 0, 0
    for (index,i) in enumerate(window_sizes)
        xi = partitioning(integrate(data1),i)
        yi = partitioning(integrate(data2),i)
        n = size(xi,1)
        m = size(xi,2)
        for j in 1:n
            #testing another version of detrending
            if order == 1
                seg_x = detrending(xi[j,:])
                seg_y = detrending(yi[j,:])
            else
                seg_x = detrending_poly(xi[j,:], order)
                seg_y = detrending_poly(yi[j,:], order)
            end
            ffi += (1/n)*((1/i)*seg_x'seg_y)
            ff1i += (1/n)*((1/i)*seg_x'seg_x)
            ff2i += (1/n)*((1/i)*seg_y'seg_y)
        end
        rho_DCCA[index] = ffi/(sqrt(ff1i)*sqrt(ff2i))
    end
    return  rho_DCCA
end
function partitioning(x::Array{Float64,1},box_size::Int64; overlap::Int = box_size - 1)
    nb_windows = div(length(x) - box_size, box_size - overlap) + 1
    partitionned_data = zeros(nb_windows, box_size)
    compteur = 1
    for i in 0:box_size - overlap:(length(x) - box_size)
        for j in 1:box_size
            partitionned_data[compteur,j] = x[i+j]
        end
        compteur += 1
    end
    return partitionned_data
end
function detrending_poly(values::Array{Float64,1}, order::Int)
    position = collect(1:length(values))
    f = Polynomials.fit(position,values,order)
    return values .- f.(position)# polyval(f,position)
end
function detrending(values::Array{Float64,1})
    x = collect(1:length(values))
    X = hcat(ones(length(values)),x)
    A = (X'*X)\X'*values
    return values .- (x.*A[2] .+ A[1])
end
function integrate(x::Array{Float64,1})
    return cumsum(x)
end
################################################################
#hourly dcca
for stock in ["GME","BB","AMC","NOK"]
    rdf = CSV.File("data/"*stock*"_input_dcca.csv")|> DataFrame
    #
    r_volume = rdf[!,"volume"]
    r_occurrences = rdf[!,"occurrences"]
    r_price = rdf[!,"price"]
    ######DCCA
    nb_pts = 30
    order = 1
    df = DataFrame()
    window_size, correlation = rhoDCCA(r_occurrences, r_occurrences;nb_pts = nb_pts, order = order)
    df[!,"window_size"] = window_size
    #
    window_size, correlation = rhoDCCA(r_price, r_volume;nb_pts = nb_pts, order = order)
    df[!,"price_volume"] = correlation
    #
    window_size, correlation = rhoDCCA(r_price, r_occurrences;nb_pts = nb_pts, order = order)
    df[!,"price_occurrences"] = correlation
    #
    window_size, correlation = rhoDCCA(r_occurrences, r_volume;nb_pts = nb_pts, order = order)
    df[!,"occurrences_volume"] = correlation
    #
    window_size, correlation = rhoDCCA(r_occurrences, r_occurrences;nb_pts = nb_pts, order = order)
    df[!,"occurrences_occurrences"] = correlation
    #
    window_size, correlation = rhoDCCA(r_price, r_price;nb_pts = nb_pts, order = order)
    df[!,"price_price"] = correlation
    #
    window_size, correlation = rhoDCCA(r_volume, r_volume;nb_pts = nb_pts, order = order)
    df[!,"volume_volume"] = correlation
    #
    #
    window_size, correlation = DCCA_coefficient(r_price, r_volume;nb_pts = nb_pts, order = order)
    df[!,"price_volume_coeff"] = correlation
    #
    window_size, correlation = DCCA_coefficient(r_price, r_occurrences;nb_pts = nb_pts, order = order)
    df[!,"price_occurrences_coeff"] = correlation
    #
    window_size, correlation = DCCA_coefficient(r_occurrences, r_volume;nb_pts = nb_pts, order = order)
    df[!,"occurrences_volume_coeff"] = correlation
    #
    window_size, correlation = DCCA_coefficient(r_occurrences, r_occurrences;nb_pts = nb_pts, order = order)
    df[!,"occurrences_occurrences_coeff"] = correlation
    #
    window_size, correlation = DCCA_coefficient(r_price, r_price;nb_pts = nb_pts, order = order)
    df[!,"price_price_coeff"] = correlation
    #
    window_size, correlation = DCCA_coefficient(r_volume, r_volume;nb_pts = nb_pts, order = order)
    df[!,"volume_volume_coeff"] = correlation
    #
    pts, ci = empirical_CI(length(r_volume))
    nci = [ci[nearest_neighbour(w,pts)[2]] for w in window_size]
    df[!,"null_hyp"] = nci
    CSV.write("data/"*stock*"_dcca.csv", df)
end