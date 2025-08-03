# Thought Process

The objective of this assessment was to reverse-engineer the actual meaning of each column in a dataset of time-series telemetry with misleading column names. The dataset contained fabricated fields: deltaX, gamma, omega, flux, pulse, and neutronCount, which represented the real field names: open, high, low, close, price, and volume.

The approach involved the following steps:

1.  **Understanding the Data:**
    *   Loading the dataset and examining the summary statistics to understand the distribution and range of each column.

2.  **Inferring Volume:**
    *   Identifying `neutronCount` as the `volume` due to its significantly higher minimum value compared to the maximum values of all other fields. Additionally, this column also has the least correlation to other columns, which in turn supports our claim.

3.  **Inferring High and Low:**
    *   Using `idxmax` and `idxmin` to find the columns with the highest and lowest values for each row, and then counting the occurrences of each column being the highest or lowest.
    *   Based on these counts, assuming `gamma` as `high` and `omega` as `low`.

4.  **Inferring Price:**
    *   Checking which of the remaining columns (`deltaX`, `pulse`, `flux`) fell between the assumed `high` and `low` values.
    *   Based on the observation that `deltaX` and `flux` always fell between `high` and `low`, while `pulse` did not, inferring `pulse` as `price`, and claimed that the initial assumption holds.

5.  **Inferring Open and Close:**
    *  We visualize the remaining columns (`deltaX` and `flux`) using from the histograms, lineplots, candlestick plots, and the manual heuristics 
    *   From the histogram, we observe that the distribution for both (`deltaX` and `flux`) columns across time is similar, showing no specific distinction.
    *  From the lineplot and candlestick plot, we observe that across time, when the slope decreases in the lineplot or red candlestick in the candlestick plot, if either of the values in the column (`deltaX` and `flux`) deterministically represent `Close`, then it is generally lesser than `Open`. Vica verse occurs during ascent. But as we can see, none of these graphs show any such trend deterministically.
    *   We developed manual heuristics based on stock market observations, such as the `Close` is expected to be the average of high, low, and price, and the correlation of `Close` with the next price and time should be high.
    *   Calculating weighted scores for each column to determine the likelihood of it being `open` or `close`, we observe that the scores have negligible difference.
    *   All of this concludes that `deltaX` and `flux` are equally probable to be `open` and `close`, hence we assign a random value to them with 0.5 confidence to each.

6.  **Validation**
    *   Although a validation script was created, it was not run in this thought process.
    *   This validation script can be extended to better validate the column assignments given historic data (over multiple days) which was absent in this assignment.

The main doubts were around assigning `open` and `close`, as the heuristics and visualizations did not provide a clear distinction between the two. A random assignment with a confidence score of 0.5 was used to address this uncertainty.
