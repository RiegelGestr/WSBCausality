library(lubridate)
library(ggplot2)
library(tibble)
library(dplyr)
library(ggbump)

# Your data
df <- tibble(
  stock = c("GME","PLTR","NIO","TSLA","AMC","NOK","BB",
            "GME","PLTR","NIO","TSLA","AMC","NOK","BB",
            "GME","PLTR","NIO","TSLA","AMC","NOK","BB",
            "GME","PLTR","NIO","TSLA","AMC","NOK","BB"
  ),
  data = c("30 Dec 2020","30 Dec 2020","30 Dec 2020","30 Dec 2020","30 Dec 2020","30 Dec 2020","30 Dec 2020",
           "13 Jan 2021","13 Jan 2021","13 Jan 2021","13 Jan 2021","13 Jan 2021","13 Jan 2021","13 Jan 2021",
           "22 Jan 2021","22 Jan 2021","22 Jan 2021","22 Jan 2021","22 Jan 2021","22 Jan 2021","22 Jan 2021",
           "27 Jan 2021","27 Jan 2021","27 Jan 2021","27 Jan 2021","27 Jan 2021","27 Jan 2021","27 Jan 2021"
  ),
  rank = c(2,1,4,3,12,13,11,
           1,3,4,2,13,12,11,
           1,4,8,3,13,12,2,
           1,6,10,5,3,4,2
  )
)

# Your color dictionary
dict_colors <- c(
  "GME" = "#B92113",
  "AMC" = "#FF8000",
  "BB" = "#FFD700",
  "NOK" = "#00CC66",
  "NIO" = "#00A8E8",
  "TSLA" = "#5E35B1",
  "PLTR" = "#28367B"
)

# Convert data$date to Date class
df$data <- dmy(df$data)

# Find min and max indices
min_index <- which.min(df$data)
max_index <- which.max(df$data)

# Create the plot
plot <- ggplot(df, aes(data, rank, color = stock)) +
  geom_point(size = 7) +
  geom_bump(size = 2, smooth = 8) +
  scale_color_manual(values = dict_colors) +  # Use manual color scale
  theme(legend.position = "none",
        panel.grid.major = element_blank()) +
  labs(y = "RANK",
       x = NULL) +
  scale_y_reverse()

# Save the plot
ggsave("fig/fig_3_a_rank.pdf", plot, width = 8, height = 4)

