using DataFrames
using CSV
using Dates
using ShiftedArrays
using Statistics
using StatsBase: autocor
using CausalityTools#1.6
using DynamicalSystems#2.3
using CairoMakie
################################################################
for stock in ["GME","AMC","BB","NOK"]
    df = CSV.File("/data/"*stock*"_julia_causality.csv")|> DataFrame
    sessions = 7
    days = 110
    df = df[sessions*days:end,:]
    x = df.volume
    y = df.occurrences
    z = df.close
    shift = 1
    r_volume = log10.(ShiftedArray(df.volume, shift)./df.volume)
    r_volume = r_volume[shift+1:end]
    r_occurrences = log10.(ShiftedArray(df.occurrences, shift)./df.occurrences)
    r_occurrences = r_occurrences[shift+1:end]
    r_price = log10.(ShiftedArray(z, shift)./z)
    r_price = r_price[shift+1:end]
    #
    r_volume = convert(Array{Float64,1},r_volume)
    r_occurrences = convert(Array{Float64,1},r_occurrences)
    r_price = convert(Array{Float64,1},r_price)
    rdf = DataFrame()
    rdf[!,"occurrences"] = r_occurrences
    rdf[!,"volume"] = r_volume
    rdf[!,"price"] = r_price
    #
    rdf.price[ismissing.(rdf.price)] .= 0
    rdf.price[isnothing.(rdf.price)] .= 0
    rdf.price[isnan.(rdf.price)] .= 0
    rdf.price[isinf.(rdf.price)] .= 0
    #
    rdf.volume[ismissing.(rdf.volume)] .= 0
    rdf.volume[isnothing.(rdf.volume)] .= 0
    rdf.volume[isnan.(rdf.volume)] .= 0
    rdf.volume[isinf.(rdf.volume)] .= 0
    #
    rdf.occurrences[ismissing.(rdf.occurrences)] .= 0
    rdf.occurrences[isnothing.(rdf.occurrences)] .= 0
    rdf.occurrences[isnan.(rdf.occurrences)] .= 0
    rdf.occurrences[isinf.(rdf.occurrences)] .= 0
    ################################################################
    #EUCLIDEAN DISTANCE ----> check metric
    ################################################################
    #estimate time delay
    τs = 1:50
    #
    autocorr_occurrences = autocor(rdf.occurrences, τs; demean=true)
    tau_occurrences_zero = estimate_delay(rdf.occurrences,"ac_zero")
    tau_occurrences_min = estimate_delay(rdf.occurrences,"ac_min")
    autocorr_volume = autocor(rdf.volume, τs; demean=true)
    tau_volume_zero = estimate_delay(rdf.volume,"ac_zero")
    tau_volume_min = estimate_delay(rdf.volume,"ac_min")
    autocorr_price = autocor(rdf.price, τs; demean=true)
    tau_price_zero = estimate_delay(rdf.price,"ac_zero")
    tau_price_min = estimate_delay(rdf.price,"ac_min")
    #
    tau_occurrences_mi = estimate_delay(rdf.occurrences,"mi_min")
    selfmutualinfo_occurrences = selfmutualinfo(rdf.occurrences,τs)
    tau_volume_mi = estimate_delay(rdf.volume,"mi_min")
    selfmutualinfo_volume = selfmutualinfo(rdf.volume,τs)
    tau_price_mi = estimate_delay(rdf.price,"mi_min")
    selfmutualinfo_price = selfmutualinfo(rdf.price,τs)
    #Plot
    fig = Figure(resolution = (1480, 1020),fontsize = 25)
    ax = Axis(fig[1,1],xlabel = "Lag", ylabel = "Autocorrelation",title=stock*" Reddit (τ = $tau_occurrences_zero)")
    l1 = lines!(ax, τs, autocorr_occurrences; lw = 50000, color = "orange",label = "Reddit")
    scatter!(ax, [tau_occurrences_zero], [autocorr_occurrences[tau_occurrences_zero]]; marker = :rect,markersize = 30, color = "pink",label = "Optimal Lag")
    axislegend(ax, position = :rb)
    ylims!(-1, 1)
    #
    ax = Axis(fig[2,1],xlabel = "Lag", ylabel = "Autocorrelation",title=stock*" Trading Volume (τ = $tau_volume_zero)")
    l1 = lines!(ax, τs, autocorr_volume; lw = 50000, color = "blue",label = "Trading V.")
    scatter!(ax, [tau_volume_zero], [autocorr_volume[tau_volume_zero]]; marker = :rect,markersize = 30, color = "pink",label = "Optimal Lag")
    axislegend(ax, position = :rb)
    ylims!(-1, 1)
    #
    ax = Axis(fig[3,1],xlabel = "Lag", ylabel = "Autocorrelation",title=stock*" Price (τ = $tau_price_zero)")
    l1 = lines!(ax, τs, autocorr_price; lw = 50000, color = "green",label = "Price")
    scatter!(ax, [tau_price_zero], [autocorr_price[tau_price_zero]]; marker = :rect,markersize = 30, color = "pink",label = "Optimal Lag")
    axislegend(ax, position = :rb)
    ylims!(-1, 1)
    #
    ################################################################
    dmax = 30
    Ds = 1:dmax
    E1_occurrences = delay_afnn(rdf.occurrences, tau_occurrences_zero,Ds)
    E2_occurrences = stochastic_indicator(rdf.occurrences, tau_occurrences_zero,Ds)
    𝒟, τ, E = optimal_traditional_de(rdf.occurrences, "afnn","ac_zero"; dmax)
    optimal_d_occurrences = size(𝒟, 2)
    #
    E1_volume = delay_afnn(rdf.volume, tau_volume_zero,Ds)
    E2_volume = stochastic_indicator(rdf.volume, tau_volume_zero,Ds)
    𝒟, τ, E = optimal_traditional_de(rdf.volume, "afnn","ac_zero"; dmax)
    optimal_d_volume = size(𝒟, 2)
    #
    E1_price = delay_afnn(rdf.price, tau_price_zero,Ds)
    E2_price = stochastic_indicator(rdf.price, tau_price_zero,Ds)
    𝒟, τ, E = optimal_traditional_de(rdf.price, "afnn","ac_zero"; dmax)
    optimal_d_price = size(𝒟, 2)
    #
    ax = Axis(fig[1,2],xlabel = "d", ylabel = "E₁",ylabelrotation = 2*pi,title = stock*" Reddit (D = $optimal_d_occurrences)")
    lines!(ax, Ds, E1_occurrences; lw = 50000, color = "red",label = "Reddit")
    scatter!(ax, [optimal_d_occurrences], [E1_occurrences[optimal_d_occurrences]]; marker = :circle,markersize = 30, color = "brown",label = "Optimal dim.")
    axislegend(ax, position = :rb)
    #
    ax = Axis(fig[2,2],xlabel = "d", ylabel = "E₁",ylabelrotation = 2*pi,title = stock*" Trading Volume (D = $optimal_d_volume)")
    lines!(ax, Ds, E1_volume; lw = 50000, color = "purple", label = "Trading V.")
    scatter!(ax, [optimal_d_volume], [E1_volume[optimal_d_volume]]; marker = :circle,markersize = 30, color = "brown",label = "Optimal dim.")
    axislegend(ax, position = :rb)
    #
    ax = Axis(fig[3,2],xlabel = "d", ylabel = "E₁",ylabelrotation = 2*pi,title = stock*" Price (D = $optimal_d_price)")
    lines!(ax, Ds, E1_price; lw = 50000, color = "black",label = "Price")
    scatter!(ax, [optimal_d_price], [E1_price[optimal_d_price]]; marker = :circle,markersize = 30, color = "brown",label = "Optimal dim.")
    axislegend(ax, position = :rb)
    #
    save("/fig/"*stock*"_time_delay.pdf", fig)
    ################################################################
end
