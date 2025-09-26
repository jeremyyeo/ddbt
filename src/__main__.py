import argparse
import re

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")
extract = subparsers.add_parser(
    "extract", help="Extract model specific log lines from debug logs."
)

extract.add_argument(
    "-f",
    "--from-file",
    required=True,
    help="The full path to the debug logs file (e.g. 'debug.log').",
)
extract.add_argument(
    "-n",
    "--node",
    required=True,
    help="The node of interest (e.g. 'model.analytics.foo').",
)
args = parser.parse_args()

# Define patterns for regex.
PATTERN_NODE_NAME = r'[a-zA-Z_]+\.[^\s"]+'
PATTERN_THREAD_NUMBER = r"Thread-(\d+)"


def build_node_index(file_name: str) -> dict:
    """Build a dict of nodes, their thread number, and the first and last log line."""
    all_nodes = {}
    with open(file_name, "r") as f:
        for line_num, line in enumerate(f):
            if "Began running node" in line:
                # Extract name of node.
                node_name = re.search(PATTERN_NODE_NAME, line).group(0)
                thread_number = re.search(PATTERN_THREAD_NUMBER, line).group(1)
                all_nodes[node_name] = {
                    "thread_number": thread_number,
                    "first_line_number": line_num,
                }
            if "Finished running node" in line:
                # Extract name of node.
                node_name = re.search(PATTERN_NODE_NAME, line).group(0)
                thread_number = re.search(PATTERN_THREAD_NUMBER, line).group(1)
                all_nodes[node_name]["last_line_number"] = line_num
    return all_nodes


def write_model_logs(all_node_index: dict, file_name: str, model_name: str) -> None:
    """Write a log file with logs specific to the model of interest."""
    with open(file_name, "r") as f:
        node_of_interest = all_node_index[model_name]
        # Extract starting from the first line to the last line.
        lines = f.readlines()[
            node_of_interest["first_line_number"] : node_of_interest["last_line_number"]
        ]
        filtered_lines = []
        keep_mode = False
        node_thread = f"Thread-{node_of_interest['thread_number']}"

        for line in lines:
            thread_match = re.search(PATTERN_THREAD_NUMBER, line)

            if node_thread in line:
                # Found a line for the node’s thread → keep it
                filtered_lines.append(line)
                keep_mode = True
            elif thread_match:
                # New thread line
                if node_thread not in line:
                    # Different thread → stop keeping continuations
                    keep_mode = False
            else:
                # Continuation (no thread number)
                if keep_mode:
                    filtered_lines.append(line)

        model_specific_log_file_name = f"{file_name}_{model_name}.log"
        with open(model_specific_log_file_name, "w") as f_write:
            f_write.writelines(filtered_lines)
        
        print(f"Model logs written to:\n{model_specific_log_file_name}")


def main():
    if args.command == "extract":
        _FILE_NAME = args.from_file
        _MODEL_NAME = args.node
        # Check file exist.
        import os.path

        if os.path.isfile(f"{_FILE_NAME}"):
            print(
                f"File '{_FILE_NAME}' found. Finding logs lines for model '{_MODEL_NAME}'."
            )
            all_node_index = build_node_index(_FILE_NAME)
            if all_node_index.get(_MODEL_NAME):
                write_model_logs(all_node_index, _FILE_NAME, _MODEL_NAME)
            else:
                print(f"Model '{_MODEL_NAME}' not found in debug logs.")
        else:
            print(f"File '{_FILE_NAME}' not found. Please confirm that the file exist.")
    else:
        print("See help by running 'ddbt -h'.")
