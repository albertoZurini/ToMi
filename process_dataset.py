import re


def fix_text(text):
    cleaned = re.sub(r"^\d{1,2}\s*", "", text, flags=re.MULTILINE)
    return "\n".join(cleaned.split("\n")[:-1])


def fix_trace(text):
    return ",".join(text.split(",")[:-2])


files = [
    "data/test.txt",
    "data/train.txt",
    "data/val.txt",
]
traces = [
    "data/test.trace",
    "data/train.trace",
    "data/val.trace",
]

all_data = []
all_traces = []

for i in range(len(files)):
    file = files[i]
    trace = traces[i]

    with open(file, "r") as f:
        data = f.read()
    with open(trace, "r") as f:
        trace = f.read()

    data = data.split("1\n")
    trace = trace.split("\n")

    all_data.extend(data)
    all_traces.extend(trace)

data_to_save = []

for i in range(len(data)):
    data_to_save.append({"story": fix_text(data[i]), "trace": fix_trace(trace[i])})
