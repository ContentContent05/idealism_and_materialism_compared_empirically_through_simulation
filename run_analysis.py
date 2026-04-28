"""
This file runs analysis by extracting important aggregate metrics, as well as plotting and exporting data.
"""


# Here are the library imports.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


# This is to direct everything exported to the proper file.
DATA_DIR = os.path.join(os.path.dirname(__file__), "sample_data")
os.makedirs(DATA_DIR, exist_ok=True)


"""
The function here in order: take in data set to make a dataframe, separate into nodes and edges to compuete,
print important aggregates and economical claims from them, and export and plot.
"""
def analysis(dataset, name):
   df = build_dataframe(dataset)
   stats_edges = compute_stats(dataset["idealism"]["edges"],
                               dataset["materialism"]["edges"])
   stats_nodes = compute_stats(dataset["idealism"]["nodes"],
                               dataset["materialism"]["nodes"])
   stats_total = compute_stats_total(dataset)
   print(f"\nEDGE ECONOMY:  Idealism avg {stats_edges['i_mean']:.2f}"
         f"  Materialism avg {stats_edges['m_mean']:.2f}"
         f"  gap {stats_edges['gap']:.2f}"
         f"  p={stats_edges['p_value']:.4f}"
         f"  d={stats_edges['cohens_d']:.3f}")
   print(f"NODE ECONOMY:  Idealism avg {stats_nodes['i_mean']:.2f}"
         f"  Materialism avg {stats_nodes['m_mean']:.2f}"
         f"  gap {stats_nodes['gap']:.2f}"
         f"  p={stats_nodes['p_value']:.4f}"
         f"  d={stats_nodes['cohens_d']:.3f}")
   print(f"TOTAL ECONOMY: Idealism avg {stats_total['i_mean']:.2f}"
         f"  Materialism avg {stats_total['m_mean']:.2f}"
         f"  gap {stats_total['gap']:.2f}"
         f"  p={stats_total['p_value']:.4f}"
         f"  d={stats_total['cohens_d']:.3f}")
   export_csv(df, name)
   plot_all(dataset, name)


"""
# This averages across runs at each time step for one representative time series.
"""
def flatten_runs(run_array):
   arr = np.array(run_array)
   return arr.mean(axis=0)


"""
This flattens everything into one long list for statistical comparison
"""
def flatten_all(run_array):
   return np.array(run_array).flatten()


"""
This creates raw, a list of totals per time step.
"""
def compute_metrics(run_array):
   arr = flatten_runs(run_array)
   return {
      "total":       arr,
      "cumulative":  np.cumsum(arr),
      "average":     np.array([arr[:i+1].mean() for i in range(len(arr))]),
      "derivative":  np.diff(arr, prepend=arr[0])
   }


"""
This t-tests by comparing the two distributions and then performs Cohen's d effect size calculations.
"""
def compute_stats(i_run_array, m_run_array):
   i = flatten_all(i_run_array)
   m = flatten_all(m_run_array)

   # The ddof=1 for sample std deviation is here, among other things.
   i_mean = np.mean(i)
   m_mean = np.mean(m)
   i_std  = np.std(i, ddof=1)
   m_std  = np.std(m, ddof=1)
   i_n    = len(i)
   m_n    = len(m)

   # Here is the pooled standard error for Welch's t-test, handling unequal variance.
   se = np.sqrt((i_std**2 / i_n) + (m_std**2 / m_n))

   # Here is the t-statistic.
   t_stat = (i_mean - m_mean) / se if se != 0 else 0.0

   # The degrees of freedom via Welch-Satterthwaite equation is ran here.
   num   = ((i_std**2 / i_n) + (m_std**2 / m_n))**2
   denom = ((i_std**2 / i_n)**2 / (i_n - 1)) + ((m_std**2 / m_n)**2 / (m_n - 1))
   df    = num / denom if denom != 0 else i_n + m_n - 2

   # Here is the p-value approximation using a normal distribution, valid for large n).
   # For large samples (ITERS * STEPS is typically large), this is reliable.
   z     = abs(t_stat)
   p_val = 2 * (1 - _normal_cdf(z))

   # Here is Cohen's d using the pooled std.
   pooled_std = np.sqrt((i_std**2 + m_std**2) / 2)
   cohens_d   = (i_mean - m_mean) / pooled_std if pooled_std != 0 else 0.0

   # This returns all the calculated numbers.
   return {
      "i_mean":   i_mean,
      "m_mean":   m_mean,
      "i_std":    i_std,
      "m_std":    m_std,
      "t_stat":   t_stat,
      "df":       df,
      "p_value":  p_val,
      "cohens_d": cohens_d,
      "gap":      m_mean - i_mean
   }


"""
# This adds nodes and edges element-wise across runs and time steps, returning the same shape as original arrays.
"""
def compute_total_series(run_array_nodes, run_array_edges):
    n = np.array(run_array_nodes)
    e = np.array(run_array_edges)
    return (n + e).tolist()


"""

"""
def compute_stats_total(dataset):
    i_total = compute_total_series(dataset["idealism"]["nodes"],
                                   dataset["idealism"]["edges"])
    m_total = compute_total_series(dataset["materialism"]["nodes"],
                                   dataset["materialism"]["edges"])
    return compute_stats(i_total, m_total)


"""

"""
def compute_metrics_total(run_array_nodes, run_array_edges):
    combined = compute_total_series(run_array_nodes, run_array_edges)
    return compute_metrics(combined)


"""
This function calculates the Abramowitz and Stegun approximation, accurate to about 7 decimal places.
"""
def _normal_cdf(z):
   t = 1 / (1 + 0.2316419 * z)
   poly = t * (0.319381530
               + t * (-0.356563782
               + t * (1.781477937
               + t * (-1.821255978
               + t * 1.330274429))))
   return 1 - (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * z**2) * poly


"""
This makes a dataframe data structure from the pandas library.
"""
def build_dataframe(dataset):
   i_e = compute_metrics(dataset["idealism"]["edges"])
   m_e = compute_metrics(dataset["materialism"]["edges"])
   i_t = compute_metrics_total(dataset["idealism"]["nodes"],
                               dataset["idealism"]["edges"])
   m_t = compute_metrics_total(dataset["materialism"]["nodes"],
                               dataset["materialism"]["edges"])
   steps = range(1, len(i_e["total"]) + 1)
   df = pd.DataFrame({
      "step":              steps,
      "i_edges_total":     i_e["total"],
      "i_edges_cumul":     i_e["cumulative"],
      "i_edges_avg":       i_e["average"],
      "i_edges_deriv":     i_e["derivative"],
      "m_edges_total":     m_e["total"],
      "m_edges_cumul":     m_e["cumulative"],
      "m_edges_avg":       m_e["average"],
      "m_edges_deriv":     m_e["derivative"],
      "i_total_total":     i_t["total"],
      "i_total_cumul":     i_t["cumulative"],
      "i_total_avg":       i_t["average"],
      "i_total_deriv":     i_t["derivative"],
      "m_total_total":     m_t["total"],
      "m_total_cumul":     m_t["cumulative"],
      "m_total_avg":       m_t["average"],
      "m_total_deriv":     m_t["derivative"],
   })
   return df


"""
This fucntion exports the data into a .csv file.
"""
def export_csv(df, name):
   path = os.path.join(DATA_DIR, f"{name}_results.csv")
   df.to_csv(path, index=False)
   print(f"Saved to {path}")


"""
This function plots all the graphs from the data.
"""
def plot_all(dataset, name):
   i_e = compute_metrics(dataset["idealism"]["edges"])
   m_e = compute_metrics(dataset["materialism"]["edges"])
   i_n = compute_metrics(dataset["idealism"]["nodes"])
   m_n = compute_metrics(dataset["materialism"]["nodes"])
   steps = range(1, len(i_e["total"]) + 1)

   # This is a time series of the average edges over time.
   plt.figure()
   plt.plot(steps, i_e["average"], label="Idealism")
   plt.plot(steps, m_e["average"], label="Materialism")
   plt.title("Average Edges Over Time")
   plt.xlabel("Time Step")
   plt.ylabel("Avg Edges")
   plt.legend()
   plt.savefig(os.path.join(DATA_DIR, f"{name}_edges_timeseries.png"))
   plt.close()

   # This is a time series of the average nodes over time.
   plt.figure()
   plt.plot(steps, i_n["average"], label="Idealism")
   plt.plot(steps, m_n["average"], label="Materialism")
   plt.title("Average Nodes Over Time")
   plt.xlabel("Time Step")
   plt.ylabel("Avg Nodes")
   plt.legend()
   plt.savefig(os.path.join(DATA_DIR, f"{name}_nodes_timeseries.png"))
   plt.close()
    
   # This is a scatter plot of nodes vs. edges per step for both models.
   plt.figure()
   plt.scatter(i_n["total"], i_e["total"], label="Idealism", alpha=0.6)
   plt.scatter(m_n["total"], m_e["total"], label="Materialism", alpha=0.6)
   plt.title("Nodes vs Edges Per Step")
   plt.xlabel("Nodes")
   plt.ylabel("Edges")
   plt.legend()
   plt.savefig(os.path.join(DATA_DIR, f"{name}_nodes_vs_edges.png"))
   plt.close()

   # Here is the derivative plot measuring the rate of change in edges over time.
   plt.figure()
   plt.plot(steps, i_e["derivative"], label="Idealism")
   plt.plot(steps, m_e["derivative"], label="Materialism")
   plt.axhline(0, color="gray", linestyle="--")
   plt.title("Edge Formation Rate (Derivative)")
   plt.xlabel("Time Step")
   plt.ylabel("Change in Edges")
   plt.legend()
   plt.savefig(os.path.join(DATA_DIR, f"{name}_edge_derivative.png"))
   plt.close()

   # This is a time series for the total economy over time.
   i_t = compute_metrics_total(dataset["idealism"]["nodes"],
                               dataset["idealism"]["edges"])
   m_t = compute_metrics_total(dataset["materialism"]["nodes"],
                               dataset["materialism"]["edges"])
   plt.figure()
   plt.plot(steps, i_t["average"], label="Idealism")
   plt.plot(steps, m_t["average"], label="Materialism")
   plt.title("Average Total Things (Nodes + Edges) Over Time")
   plt.xlabel("Time Step")
   plt.ylabel("Avg Total")
   plt.legend()
   plt.savefig(os.path.join(DATA_DIR, f"{name}_total_timeseries.png"))
   plt.close()

   # This makes a bar chart to summarize stats side by side.
   labels = ["Idealism", "Materialism"]
   node_means  = [np.mean(i_n["total"]), np.mean(m_n["total"])]
   edge_means  = [np.mean(i_e["total"]), np.mean(m_e["total"])]
   total_means = [np.mean(i_t["total"]), np.mean(m_t["total"])]
   x = np.arange(2)
   plt.figure()
   plt.bar(x - 0.27, node_means,  width=0.27, label="Avg Nodes")
   plt.bar(x,        edge_means,  width=0.27, label="Avg Edges")
   plt.bar(x + 0.27, total_means, width=0.27, label="Avg Total")
   plt.xticks(x, labels)
   plt.title("Economy Comparison")
   plt.ylabel("Count")
   plt.legend()
   plt.savefig(os.path.join(DATA_DIR, f"{name}_economy_summary.png"))
   plt.close()