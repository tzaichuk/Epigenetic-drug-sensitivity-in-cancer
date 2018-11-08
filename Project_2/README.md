# Project2

Epigenetic drug sensitivity in cancer.

Alterations in cancer genomes strongly influence clinical responses to treatment and in many instances are potent biomarkers for response to drugs. The Genomics of Drug Sensitivity in Cancer (GDSC) database (www.cancerRxgene.org) is the largest public resource for information on drug sensitivity in cancer cells and molecular markers of drug response. Data are freely available without restriction. GDSC currently contains drug sensitivity data for almost 75 000 experiments, describing response to 138 anticancer drugs across almost 950 cancer cell lines. To identify molecular markers of drug response, cell line drug sensitivity data are integrated with large genomic datasets obtained from the Catalogue of Somatic Mutations in Cancer database, including information on somatic mutations in cancer genes, gene amplification and deletion, tissue type and transcriptional data. Analysis of GDSC data is through a web portal focused on identifying molecular biomarkers of drug sensitivity based on queries of specific anticancer drugs or cancer genes. 
First step: Understand the data I am trying to visualize, including its size and cardinality (the uniqueness of data values in a column)
Problem statement: Compare epigenetic compounds efficiency IC50 9The IC50 is the concentration of an inhibitor where the response (or binding) is reduced by half) by tissue subtype.
I used Pandas and sqlalchemy to import the CSV data, Plotly in Javascript for visualization, Python Flask for running. final visualization
https://tzaichuk-project2.herokuapp.com/.
Challenges: I learned how to create an end to end application using big data processing (querying datasets) and visualization
build a dashboard to visualize processed data. 

