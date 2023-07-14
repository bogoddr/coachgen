import sys
import os

if len(sys.argv) < 3:
    print("Usage: python coachgen.py <path to chart> <path to labels>")
    print("Example: python coachgen.py data/coachorders.sm data/coachorders_labels.txt")
    sys.exit(1)

filepath_chart = sys.argv[1]
filepath_labels = sys.argv[2]

# Utils

def read_file(filename):
    with open(filename, 'r') as file:
        file_string = file.read()
    return file_string

def read_file_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return lines

def read_file_binary(filename):
    with open(filename, "rb") as f:
        data = f.read()
    return data

def write_file_binary(output_path, data):
    with open(output_path, "wb") as f:
        f.write(data)

def write_file_string(output_path, s):
    with open(output_path, "w") as text_file:
        text_file.write(s)

def create_directory(directory_path):
    try:
        # Create a directory
        os.mkdir(directory_path)
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists!")
    except Exception as e:
        print(f"An error occurred while creating the directory: {str(e)}")

# Chart creation

def parse_labels(labels):
    labels_parsed = []
    for label in labels:
        print(label)
        measures = label.split(":")[0].split('-')
        name = label.split(":")[1]
        labels_parsed.append({
            "measures_start": int(measures[0]),
            "measures_end": int(measures[1]),
            "name": name
        })
    return labels_parsed

def parse_chart(chartfile):
    chartfile = chartfile.split('     0,0,0,0,0:')[1]
    chartfile = chartfile.split(';')[0]
    chartfile = chartfile.strip()
    measures = chartfile.split(',')
    return {
        "measures": measures
    }

def get_measures_from_source_chart(source_chart, start, end):
    selected_measures = ''
    for measure in range(start, end + 1):
        measure_notes = source_chart['measures'][measure]
        selected_measures += measure_notes + "\n,"
    return selected_measures

def build_chart(source_chart, label, blank_chart, audio, mode):
    name = label['name'] + '__' + mode
    chart_dir = 'output/' + 'coachgen_' + name
    create_directory(chart_dir)

    selected_measures = ''

    if ("WARMUP" in mode):
        footspeed_warmup_measures = get_measures_from_source_chart(source_chart, 0, 3)
        selected_measures = selected_measures + footspeed_warmup_measures

    start = label["measures_start"]
    end = label["measures_end"]
    measures_from_chart = get_measures_from_source_chart(source_chart, start, end)
    selected_measures = selected_measures + measures_from_chart
    if (("SPEEDUP" in mode) or ("REPEAT_10X" in mode)):
        for i in range(0,10):
            selected_measures = selected_measures + measures_from_chart
    if ("REPEAT_3X" in mode):
        for i in range(0,3):
            selected_measures = selected_measures + measures_from_chart

    chart = blank_chart.replace("<%NAME%>", name)
    chart = chart.replace("<%CHART%>", selected_measures)

    if ("SPEEDUP" in mode):
        chart = chart.replace("<%BPMS%>", "0.000=120.000\n,16.000=130.000\n,32.000=140.000\n,48.000=150.000\n,64.000=160.000\n,80.000=170.000\n,96.000=180.000\n,112.000=190.000\n,128.000=200.000\n,144.000=210.000\n,160.000=220.000\n,")
    else:
        chart = chart.replace("<%BPMS%>", "0.000=150.000")

    write_file_string(chart_dir + '/' + name + '.sm', chart)
    write_file_binary(chart_dir + '/' + 'none.ogg', audio)

labels = parse_labels(read_file_lines(filepath_labels))
chart = parse_chart(read_file(filepath_chart))
blank_chart = read_file('resources/blank.sm')
audio = read_file_binary('resources/none.ogg')

for label in labels:
    #build_chart(chart, label, blank_chart, audio, '')
    build_chart(chart, label, blank_chart, audio, 'WARMUP')
    build_chart(chart, label, blank_chart, audio, 'SPEEDUP')
    #build_chart(chart, label, blank_chart, audio, 'REPEAT_3X')
    #build_chart(chart, label, blank_chart, audio, 'REPEAT_10X')
    build_chart(chart, label, blank_chart, audio, 'WARMUP_REPEAT_3X')
    build_chart(chart, label, blank_chart, audio, 'WARMUP_REPEAT_10X')
