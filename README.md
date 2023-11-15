
# **IMGTB: Integrated MGTBench Framework**
A machine-generated text benchmarking framework, heavily based upon the original [MGTBench project](https://github.com/xinleihe/MGTBench), featuring additional funcionalities that make it easier to integrate custom datasets and new custom detection methods. 

The framework also includes a couple of analysis tools for automatic analysis of the benchmark results.
Namely, currently we are able to visualize:
- Multiple metrics (Accuracy, Precision, Recall, F1 score) evaluated on the test data partition
- F1 score for multiple different text length groups
- Per-method (per-dataset) running time, running time over multiple datasets
- Prediction probability histogram
- Prediction probability error histogram (how often and by how much is the prediction off)

## **Supported Methods**
Currently, we support the following methods. To add a new method you can see the documentation below:
- Metric-based methods:
    - Log-Likelihood [[Ref]](https://arxiv.org/abs/1908.09203);
    - Rank [[Ref]](https://arxiv.org/abs/1906.04043);
    - Log-Rank [[Ref]](https://arxiv.org/abs/2301.11305);
    - Entropy [[Ref]](https://arxiv.org/abs/1906.04043);
    - GLTR Test 2 Features (Rank Counting) [[Ref]](https://arxiv.org/abs/1906.04043);
    - DetectGPT [[Ref]](https://arxiv.org/abs/2301.11305);
    - DetectLLM-LLR [[Ref]](https://arxiv.org/abs/2306.05540);
    - DetectLLM-NPR [[Ref]](https://arxiv.org/abs/2306.05540);
    - Multi-Feature Detection [[Ref]](https://www.researchsquare.com/article/rs-3226684/v1)
    - LLM Deviation [[Ref]](https://www.researchsquare.com/article/rs-3226684/v1)
- Model-based methods:
    - RoBERTa Base OpenAI Detector [[Ref]](https://huggingface.co/roberta-base-openai-detector)
    - RoBERTa Large OpenAI Detector [[Ref]](https://huggingface.co/roberta-large-openai-detector)
    - ChatGPT-detector-RoBERTa [[Ref]](https://huggingface.co/Hello-SimpleAI/chatgpt-detector-roberta)
    - detection-longformer [[Ref]](https://huggingface.co/nealcly/detection-longformer)
    - arincon/roberta-base-autextification-detection [[Ref]](https://huggingface.co/arincon/roberta-base-autextification-detection)
    - orzhan/ruroberta-ruatd-binary [[Ref]](https://huggingface.co/orzhan/ruroberta-ruatd-binary)
    - andreas122001/roberta-mixed-detector [[Ref]](https://huggingface.co/andreas122001/roberta-mixed-detector)
    - Any other HuggingFace text classification model
- Other
    - GPTZero [[Ref]](https://gptzero.me/)

## **Installation**

```bash
git clone https://github.com/michalspiegel/IMGTB.git;
cd IMGTB;
conda env create -f environment.yaml;
conda activate IMGTB;
```

## **Usage**
To run the benchmark on the SQuAD1 dataset: 
```python
# Distinguish Human vs. ChatGPT - by default runs all methods:
python benchmark.py --dataset datasets/SQuAD1_LLMs.csv auto SQuAD1 text label 0 ChatGPT

# Run only selected methods
python benchmark.py --dataset datasets/SQuAD1_LLMs.csv auto SQuAD1 text label 0 ChatGPT --methods RankMetric EntropyMetric
```

## **Configuration**
You can specify parameters for the benchmark run in two ways:

- Use command-line arguments
- Create a YAML configuration file

### **Command-line arguments**
To see a summarization of all of the command-line arguments and options, see either the help message or the `lib/config.py` source file.
### **YAML configuration file** 
See example configuration file at `example_config.yaml` explaining most of the available features, or see `lib/default_config.yaml` to see all currently supported parameters.
## **Support for custom dataset integration**
### **Dataset parameters**
In the CLI you will have to define a path to your dataset file (or a folder, if your dataset is constructed from multiple files).

You can define multiple datasets, that way your chosen MGTD methods will be evaluated against multiple datasets. To define more than one dataset use the `--dataset` option for each dataset. E.g.:
```bash
python benchmark.py --dataset datasets/test_dataset.csv --dataset datasets/test_dataset2.csv
```
The general dataset definition or usage of the `--dataset` option would be:
```bash
--dataset FILEPATH FILETYPE PROCESSOR TEXT_FIELD LABEL_FIELD HUMAN_LABEL OTHER
```
Only required parameter is the dataset filepath, other parameters will be filled in with their default values, if left empty.

### **Supported dataset formats**
We currently support all filetypes listed below, together with the following formats:
- Default processor can parse Hugging Face Hub datasets,  all table data with separate columns for text and label
- Use different splits
    - Different train-test split percentage
    - Different splits, configurations for Hugging Face Hub datasets
- Test on machine/human only text by specifying predefined machine/human only dataset processing function

#### **Supported dataset filetypes**
- auto
- csv
- tsv
- xls
- xlsx
- json
- jsonl
- xml
- huggingfacehub

### **Dataset processors**
In the CLI you also have to define a processor which will be a function that will process your selected dataset files into a unified data format. Unless you leave it on default, which takes your input dataset (that should constitute of a single file) and parses it using '--text_field' and '--label_field' (user-specified or the default) CLI arguments.

### **Processor definition**
In case the provided functionality for parsing datasets is not enough, it is possible to define your own dataset processing function.
A processor is a function defined in the `dataset_loader.py` source file as follows:

**Name:** process_PROCESSOR-NAME (Here, PROCESSOR-NAME will be the selected name of your processor. This would be usually the name of the dataset)

**Input:** 2 arguments: list of pandas dataframes for each dataset file, configuration dictionary holding the specifics configuration for the currently processed dataset 

**Output:** a dictionary of the following form: `{"train": {"text": ["example texts here...", "multiple.."], "label": [1,0,..]} , "test": {"text": ["example texts here...", "multiple.."], "label": [1,0,..]}}`

**Examples usage could be:**

```bash
python benchmark.py --dataset datasets/test_dataset.csv
python benchmark.py --dataset datasets/test_dataset.csv csv myAwesomeTestProcessor
python benchmark.py --dataset datasets/test_dataset.csv csv myAwesomeTestProcessor ThisIsTextFieldName ThisIsLabelFieldName Human OtherTextDataToBePassedToProcessor
```

This will tie to the `process_myAwesomeDatasetProcessor()` function (it must be implemented beforehand) that will be given the raw content of `datasets/test_dataset.csv`.

## **Support for custom MGTD method integration**

To integrate a new method, you need to define new `Experiment` subclass in the `methods/implemented_methods directory`. The main script in `benchmark.py` will automatically detect (unless you choose otherwise by configuring the `--methods` option) your new method and evaluate it on your chosen dataset.

### **How to implement a new Experiment subclass**

To implement a new method, you can use one of the templates in the `methods/method_templates`. You will just have to fill in the not yet implemented methods and maybe tweak the `__init__()` constructor. 

Remember to always implement the `run()` method (sometimes it's implemented in the parent class). It should always return a JSON-compatible dictionary of results as is defined below.

### **Experiment output format**
Each experiment run should return a JSON-compatible dictionary with results with at least the following items:
- name - name of the experiment
- input_data - the data, texts, labels that the method was trained/evaluated on, usually split into train and test sections
- predictions - predicted labels
- machine_prob - predicted probability that a given text is machine-generated
- metrics_results - evaluation of different classification metrics (e.g. Accuracy, Precision, F1...), usually split into train and test sections

### **Support for Text Clasisfication Hugging Face Hub models**
Aside from locally defined Experiment classes, you can specify a Hugging Face Hub Text Classification model as the name of the method in three different ways:
1. a string with the shortcut name of a pre-trained model to load from cache or download, e.g.: bert-base-uncased
2. a string with the identifier name of a pre-trained model that was user-uploaded to our S3, e.g.: dbmdz/bert-base-german-cased
3. a path to a directory containing model weights saved using save_pretrained(), e.g.: ./my_model_directory/

#### **Note**:
While developing your new method, you might find useful some of the functionality in `methods/utils.py`

## **How are benchmark results stored?** 
Results of every benchmark run, together with the command-line parameters, will be logged in the `results/logs` folder.

At the same time, results of each method and dataset combination will be saved in the `results/methods` folder. (In this way, you will be able to see the results of individual method and dataset experiment runs with different parameters together in one place)

## **Results analysis**

> :warning: Currently it is only possible to run analysis on logs (whole benchmark results). Support for the analysis of the separate method/dataset results will be added.

Results analysis will be run after each benchmark run.

Or you can run analysis from a log manually, specifying the benchmark log filepath and save path to store the analysis results:
```bash
results_analysis.py results/logs/SOME_BENCHMARK_RESULTS.json SAVE_PATH
```

Currently, we are able to visualize:
- Multiple metrics (Accuracy, Precision, Recall, F1 score) evaluated on the test data partition
- F1 score for multiple different text length groups
- Prediction Probability Distribution - How much and how often is the detection method sure of its predictions
- Prediction Probability Error Distribution - How far was the prediction from true label, how often
- False Positives Analysis - Analyzes the predictions for solely the negative samples. It uses the following terminology:
    | Label |                          |  Prediction Probability |
    | ----- | ------------------------ | -------------- |
    | TN    | True Negative            | 0-20% machine  |
    | PTN   | Partially True Negative  | 20-40% machine |
    | UNC   | Unclear                  | 40-60% machine |
    | PFP   | Partially False Positive | 60-80% machine |
    | FP    | False Positive           | 80-100% machine|

- False Negatives Analysis - Analyzes the predictions for solely the positive samples. It uses the following terminology:
    | Label |                           |  Prediction Probability |
    | ----- | ------------------------- | -------------- |
    | FN    | False Negative            | 0-20% machine  |
    | PFN   | Partially False Negative  | 20-40% machine |
    | UNC   | Unclear                   | 40-60% machine |
    | PTP   | Partially True Positive   | 60-80% machine |
    | TP    | True Positive             | 80-100% machine|
- Per-method per-dataset running time
- Per-method running time over multiple datasets

You can add your own analysis method by defining it in the `results_analysis.py` source file.


## **Authors**
The framework was built upon the original [MGTBench project](https://github.com/xinleihe/MGTBench), designed and developed by Michal Spiegel (KINIT) under the supervision of Dominik Macko (KINIT). 

Credit for the original MGTBench tool, created as a part of the [MGTBench: Benchmarking Machine-Generated Text Detection](https://arxiv.org/abs/2303.14822) paper, goes to its original designers and developers: Xinlei He (CISPA), Xinyue Shen (CISPA), Zeyuan Chen (Individual Researcher), Michael Backes (CISPA), and Yang Zhang (CISPA).