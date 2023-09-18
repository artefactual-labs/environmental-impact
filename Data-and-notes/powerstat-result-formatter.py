import argparse
import re

def process_file(input_file_path, output_file_path):
    try:
        # Open the input file for reading
        with open(input_file_path, 'r') as input_file:
            # Read all lines from the input file
            lines = input_file.readlines()

        # Open the output file for writing
        with open(output_file_path, 'w') as output_file:
            # Flag to track the first "  Time" line
            first_time_line_encountered = False

            # Flag to stop processing if "Summary:" is encountered
            stop_processing = False

            # Process each line and write to the output file
            for line in lines:
                if line.startswith("Summary:"):
                    # Stop processing when "Summary:" is encountered
                    stop_processing = True
                    break
                elif line.startswith("  Time") and not first_time_line_encountered:
                    # Include the first "  Time" line in the output
                    first_time_line_encountered = True
                    processed_line = re.sub(r'\s+', ',', line.strip())
                    if processed_line:  # Check if the processed line is not empty
                        output_file.write(processed_line + '\n')
                elif not line.startswith("  Time") and \
                     not line.startswith("Running for ") and \
                     not line.startswith("Power measurements will ") and \
                     not line.startswith("---"):
                    # Replace one or more spaces with a single comma
                    processed_line = re.sub(r'\s+', ',', line.strip())
                    if processed_line:  # Check if the processed line is not empty
                        output_file.write(processed_line + '\n')

            if stop_processing:
                print(f"Processing stopped at 'Summary:' in '{input_file_path}'")

        print(f"File processed successfully from '{input_file_path}' to '{output_file_path}'")

    except FileNotFoundError:
        print(f"Error: File not found - '{input_file_path}'")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description="Process PowerStat results file and save the result as a CSV.")
    
    # Add arguments for input and output file names
    parser.add_argument("powerstat_results_file", help="PowerStat results file name")
    parser.add_argument("powerstat_results_csv", help="PowerStat results CSV file name")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Process the files based on user input
    process_file(args.powerstat_results_file, args.powerstat_results_csv)

