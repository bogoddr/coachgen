# coachgen

Practice chart generator for Stepmania. Takes a source chart and splits it into individual charts based on a list of segments provided, with bonus features such as repeating sections, adding a warmup section, gradual speed increments to build better muscle memory, etc.

For an example of what the program spits out, see [sample_output.rar](https://github.com/bogoddr/coachgen/raw/master/sample_output.rar) (contains a bunch of charts, drag the folder into Stepmania's Songs director)

## Usage

```
python coachgen.py <source chart> <labels>
```

Where `<source chart>` is a `.sm` file and `labels` is a text file in [this format](https://github.com/bogoddr/coachgen/blob/master/data/coachorders_labels.txt) that describes how to split the chart.

Example usage:

```
python coachgen.py data/coachorders.sm data/coachorders_labels.txt
```
