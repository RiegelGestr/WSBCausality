using DataFrames
using CSV
using Dates
using ShiftedArrays
using Statistics
using StatsBase: crosscor
using CausalityTools#1.6
using DynamicalSystems#2.3
using CairoMakie
################################################################
for stock in ["GME","AMC","BB","NOK"]
    df = CSV.File("/data/"*stock*"_input_ccm.csv")|> DataFrame
    ##############################################################################################
    taus = 5:8
    dimensions = 4:7
    #
    libsizes = [20:1:100;120:2:240; 250:10:500;500:50:750]
    for tau in taus
        for dimension in dimensions
            fig = Figure(resolution = (1480, 1020),fontsize = 25)
            #Reddit-Volume
            x = rdf.occurrences
            y = rdf.volume
            m_ccm = ConvergentCrossMapping(d = dimension,τ = -tau)
            est = ExpandingSegment(; libsizes)
            ensemble_rv = Ensemble(m_ccm, RandomVectors(; libsizes); nreps = 50)
            #ρs_x̂y = crossmap(m_ccm, est, x, y)
            #ρs_ŷx = crossmap(m_ccm, est, y, x)
            ρs_x̂y = mean.(crossmap(ensemble_rv, x, y))
            ρs_ŷx = mean.(crossmap(ensemble_rv, y, x))
            #simple crosscorrelation
            crosscorr = crosscor(x,y,[i for i in libsizes])
            #
            ax = Axis(fig[1,1:2],xlabel = "Library Size T", ylabel = "Correlation ρ",title=stock*"(τ = $tau, d = $dimension)")
            ylims!(ax, (-1, 1))
            scatterlines!(libsizes, ρs_x̂y, label = "Reddit -> Trading V.", color = "#EF6939")
            scatterlines!(libsizes, ρs_ŷx, label = "Trading V. -> Reddit", color = "#004E89")
            axislegend(ax, position = :rb)
            #Volume-Price
            x = rdf.price
            y = rdf.volume
            m_ccm = ConvergentCrossMapping(d = dimension,τ = -tau)
            est = ExpandingSegment(; libsizes)
            ensemble_rv = Ensemble(m_ccm, RandomVectors(; libsizes); nreps = 50)
            #ρs_x̂y = crossmap(m_ccm, est, x, y)
            #ρs_ŷx = crossmap(m_ccm, est, y, x)
            ρs_x̂y = mean.(crossmap(ensemble_rv, x, y))
            ρs_ŷx = mean.(crossmap(ensemble_rv, y, x))
            ax = Axis(fig[1,3:4],xlabel = "Library Size T", ylabel = "Correlation ρ",title=stock*"(τ = $tau, d = $dimension)")
            ylims!(ax, (-1, 1))
            scatterlines!(libsizes, ρs_x̂y, label = "Price -> Trading V.", color = "#2BD9CA")
            scatterlines!(libsizes, ρs_ŷx, label = "Trading V. -> Price", color = "#5A41D9")
            axislegend(ax, position = :rb)
            #Price-Reddit
            x = rdf.price
            y = rdf.occurrences
            m_ccm = ConvergentCrossMapping(d = dimension,τ = -tau)
            est = ExpandingSegment(; libsizes)
            ensemble_rv = Ensemble(m_ccm, RandomVectors(; libsizes); nreps = 50)
            #ρs_x̂y = crossmap(m_ccm, est, x, y)
            #ρs_ŷx = crossmap(m_ccm, est, y, x)
            ρs_x̂y = mean.(crossmap(ensemble_rv, x, y))
            ρs_ŷx = mean.(crossmap(ensemble_rv, y, x))
            ax = Axis(fig[1,5:6],xlabel = "Library Size T", ylabel = "Correlation ρ",title=stock*"(τ = $tau, d = $dimension)")
            ylims!(ax, (-1, 1))
            scatterlines!(libsizes, ρs_x̂y, label = "Price -> Reddit", color = "#70ADE9",ls = :dash)
            scatterlines!(libsizes, ρs_ŷx, label = "Reddit -> Price", color = "#DB4375",ls = :dash)
            axislegend(ax, position = :rb)
            #
            save("/fig/"*stock*"_lag_"*string(tau)*"_dim_"*string(dimension)*".pdf", fig)
        end
    end
end
