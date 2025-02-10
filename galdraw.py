# Drawing parameters for the Galois LFSR visualization
# Note: All parameters are independent to provide flexibility in customization
# For example: you can adjust line thickness or box sizes independently

# Background color
backgroundColor = "white"

# Border size around the figure in mm
borderSize = 15

# Line widths
lineWidth = "0.1"  # Standard line width for boxes and connections
circleLineWidth = "0.12"  # Slightly thicker for XOR circles
arrowHead = "0.5"


# Size of the LFSR box cm (adjusted based on length)
def get_box_size(length):
    if length <= 8:
        return 4
    elif length <= 16:
        return 2.5
    else:
        return 2


# box Color use Tikz format
boxColor = "{{rgb:black,0;white,5}}"

# used for the distance of the box variable names
boxBelowTextDistance = 6

# size of the x-or drawing cm
xorSize = 1


# Get font size based on box size
def get_font_size(box_size):
    scale = box_size / 4.0
    return f"{int(30 * scale)}pt"


# Global variables for drawing
drawInitValues = True  # Show values in boxes
printBoxNames = True  # Show box names

# These will be set based on LFSR length
boxSize = 4  # Default box size
xorDistance = 2  # Default XOR distance
BoxValuesFontSize = "30pt"  # Default font sizes
BoxIndexFontSize = "20pt"

# Starting position of the first box
x = 25
y = 20

# Distance the feedback line extends to the left (will be set based on box size)
leftFeedbackDistance = 8


# LaTeX preamble for standalone TikZ
def printPreample():

    print(
        "\\documentclass[magick={density=300,size=1080x800,outext=.png},tikz]{standalone}"
    )

    print("\\usepackage{xcolor}")
    print("\\usepackage{scalerel}")
    print("\\usepackage{amsmath}")
    print("\\usetikzlibrary{arrows.meta,backgrounds}")
    print(
        "\\tikzset{{white background/.style={{show background rectangle,tight background,background rectangle/.style={{fill={0} }} }} }}".format(
            backgroundColor
        )
    )
    print("")
    print("\\begin{document}")
    print("\\begin{tikzpicture}[white background]\n\n")


# LaTeX end
def printPrologue():
    # https://tex.stackexchange.com/a/596158/62865
    print(
        "\\path (current bounding box.north east) +({0}mm,{0}mm) (current bounding box.south west) +(-{0}mm,-{0}mm);".format(
            borderSize
        )
    )
    print("\n\\end{tikzpicture}")
    print("\\end{document}")


# Prints the Galois LFSR boxes. If printBoxNames is True, box names are also printed
def printGaloisRegister(x1, y1, value, index):

    print("%node {0}".format(index))

    if drawInitValues:
        if printBoxNames:
            print(
                "\\draw node[draw, fill={8}, minimum size={3}cm,line width={4}cm, label={{ [yshift=-{9}cm] {{ $\\scaleto{{x_{{ {7} }} }}{{ {6} }}$ }} }} ] at ({0}, {1}) {{ $\\scaleto{{ {2} }}{{ {5} }}$ }};".format(
                    x1,
                    y1,
                    value,
                    boxSize,
                    lineWidth,
                    BoxValuesFontSize,
                    BoxIndexFontSize,
                    index,
                    boxColor,
                    boxBelowTextDistance,
                )
            )
        else:
            print(
                "\\draw node[draw, fill={7}, minimum size={3}cm,line width={4}cm] at ({0}, {1}) {{ $\\scaleto{{ {2} }}{{ {5} }}$ }};".format(
                    x1,
                    y1,
                    value,
                    boxSize,
                    lineWidth,
                    BoxValuesFontSize,
                    BoxIndexFontSize,
                    boxColor,
                )
            )
    else:
        if printBoxNames:
            print(
                "\\draw node[draw, fill={8}, minimum size={3}cm,line width={4}cm, label={{ [yshift=-{9}cm] {{ $\\scaleto{{x_{{ {7} }} }}{{ {6} }}$ }} }} ] at ({0}, {1}) {{ }} ;".format(
                    x1,
                    y1,
                    value,
                    boxSize,
                    lineWidth,
                    BoxValuesFontSize,
                    BoxIndexFontSize,
                    index,
                    boxColor,
                    boxBelowTextDistance,
                )
            )
        else:
            print(
                "\\draw node[draw, fill={7}, minimum size={3}cm,line width={4}cm] at ({0}, {1}) {{ }};".format(
                    x1,
                    y1,
                    value,
                    boxSize,
                    lineWidth,
                    BoxValuesFontSize,
                    BoxIndexFontSize,
                    boxColor,
                )
            )


# Draws a line from a register to the XOR gate for Galois LFSR tap points
def printGaloisTapLine(x1, y1, length, arrow=False):
    # Draw line up to feedback line position
    feedback_y = y1 + length + xorSize  # Use the provided length parameter directly
    print(
        "\t\\draw [line width={0}cm]({1},{2}) -- ({1},{3});".format(
            lineWidth, x1, y1, feedback_y
        )
    )

    # Make the half circle smaller
    radius = boxSize / 6

    # Add half circle connecting to the square, flipped on x-axis
    print(
        "\t\\draw [line width={0}cm] ({1},{2}) arc(180:0:{3});".format(
            lineWidth, x1 - radius, y1, radius
        )
    )

    # Position arrow to point exactly to the half circle
    arrow_start_y = y1 + radius * 3  # Start position
    arrow_end_y = y1 + radius  # End position at exact top of half circle
    print(
        "\t\\draw [arrows={{-Triangle[angle=90:{0}cm,black,fill=black,line width={1}cm]}}]({2},{3}) -- ({2},{4});".format(
            arrowHead, lineWidth, x1, arrow_start_y, arrow_end_y
        )
    )


def printGaloisFeedbackPath(x1, x2, x3, y1, y2, feedback, boxsizehalf):
    if drawInitValues:
        print(
            "\\draw[->,line width=0.1cm,arrows={{-Triangle[angle=90:{6}cm,black,fill=black,line width={5}cm]}}] ({0},{3}) -- ({1},{3}) -- ({1},{4}) -- node[above,yshift={9}cm] {{ $\\scaleto{{ {8} }}{{ {7} }}$ }}  ({2},{4});".format(
                x1,
                x2,
                x3,
                y1,
                y2,
                lineWidth,
                arrowHead,
                BoxValuesFontSize,
                feedback,
                boxsizehalf,
            )
        )
    else:
        print(
            "\\draw[->,line width=0.1cm,arrows={{-Triangle[angle=90:{6}cm,black,fill=black,line width={5}cm]}}] ({0},{3}) -- ({1},{3}) -- ({1},{4}) -- ({2},{4});".format(
                x1,
                x2,
                x3,
                y1,
                y2,
                lineWidth,
                arrowHead,
                BoxValuesFontSize,
                feedback,
                boxsizehalf,
            )
        )


def printGaloisOutput(x1, x2, y1, value, boxsizehalf):
    if drawInitValues:
        print(
            "\\draw[->,line width=0.1cm,arrows={{-Triangle[angle=90:{4}cm,black,fill=black,line width={3}cm]}}] ({0},{2}) -- ({1},{2}) node[midway,above,yshift={7}cm]{{  $\\scaleto{{  {6}  }}{{ {5} }}$  }};".format(
                x1, x2, y1, lineWidth, arrowHead, BoxValuesFontSize, value, boxsizehalf
            )
        )
    else:
        print(
            "\\draw[->,line width=0.1cm,arrows={{-Triangle[angle=90:{4}cm,black,fill=black,line width={3}cm]}}] ({0},{2}) -- ({1},{2}) node[midway,above]{{}};".format(
                x1, x2, y1, lineWidth, arrowHead, BoxValuesFontSize
            )
        )


# Feedback calculator for the Galois LFSR
def calculateGaloisFeedback(taps, values):
    feedback = 0
    for i, tap in enumerate(taps):
        if tap == 1:
            feedback = feedback ^ values[i]
    return feedback


# Main function to print the complete LFSR diagram
def drawGaloisLFSR(taps, values, hideValues, hideBoxNames):
    global drawInitValues, printBoxNames
    global boxSize, xorDistance, BoxValuesFontSize, BoxIndexFontSize, leftFeedbackDistance

    # Update drawing parameters based on LFSR length
    boxSize = get_box_size(len(taps))
    xorDistance = boxSize / 2
    BoxValuesFontSize = get_font_size(boxSize)
    BoxIndexFontSize = get_font_size(boxSize)

    leftFeedbackDistance = 2 * boxSize

    drawInitValues = not hideValues
    printBoxNames = not hideBoxNames

    lastTapPos = 0
    printPreample()
    count = taps.count(1)

    for i, val in enumerate(taps):
        printGaloisRegister(x + i * boxSize, y, values[i], i)

        if val == 1:
            # Draw tap lines with standard height
            printGaloisTapLine(x + i * boxSize, y + boxSize / 2, xorDistance)

            # For the last box, add the output feedback line going to the top feedback line
            if i == len(taps) - 1:
                # Calculate the coordinates for the output feedback line
                box_right_x = x + i * boxSize + boxSize  # Right edge of the last box
                feedback_y = (
                    y + boxSize / 2 + xorDistance + xorSize
                )  # Height of the feedback line
                # Draw line up and left to connect to feedback line
                print(
                    "\\draw [line width={0}cm] ({1},{2}) -- ({1},{3}) -- ({4},{3});".format(
                        lineWidth,
                        box_right_x,  # Start just right of the last box
                        y,  # Start at output line height
                        feedback_y,  # Go up to feedback line height
                        x - leftFeedbackDistance,  # Go left to meet feedback line
                    )
                )
                printGaloisTapLine(x + i * boxSize, y + boxSize / 2, xorDistance)
            count = count - 1
            lastTapPos = i

    feedbackValue = calculateGaloisFeedback(taps, values)
    printGaloisFeedbackPath(
        x + (lastTapPos) * boxSize,  # x1
        x - leftFeedbackDistance,  # x2
        x - boxSize / 2,  # x3
        y + boxSize / 2 + xorDistance + xorSize,  # y1
        y,  # y2
        feedbackValue,  # Feedback value
        boxSize / 4,  # Box size for position of the feedback value
    )

    printGaloisOutput(
        x + (len(taps) - 1) * boxSize + boxSize / 2,
        x + (len(taps) - 1) * boxSize + 2 * boxSize,
        y,
        values[-1],
        boxSize / 4,
    )

    printPrologue()


def parse_binary_list(s):
    """Convert a string of 1s and 0s into a list of integers."""
    try:
        return [int(x) for x in s if x in "01"]
    except ValueError:
        raise argparse.ArgumentTypeError("Input must be a string of 0s and 1s")


def compile_and_convert(output_format="pdf"):
    """Compile LaTeX and convert to specified format."""
    import subprocess
    from pathlib import Path

    outputs = []

    # Convert LaTeX to PDF
    try:
        subprocess.run(
            ["pdflatex", "-interaction=batchmode", "lfsr.tex"],
            capture_output=True,
            check=True,
        )
        outputs.append("lfsr.pdf")

        # Generate other formats if requested
        if output_format in ["eps", "all"]:
            subprocess.run(
                ["pdftops", "-eps", "lfsr.pdf", "lfsr.eps"],
                capture_output=True,
                check=True,
            )
            outputs.append("lfsr.eps")

        if output_format in ["png", "all"]:
            subprocess.run(
                ["magick", "-density", "300", "lfsr.pdf", "lfsr.png"],
                capture_output=True,
                check=True,
            )
            outputs.append("lfsr.png")

        # Clean up temporary files
        for f in Path(".").glob("lfsr.*"):
            if f.suffix in [".aux", ".log", ".tex"]:
                f.unlink()
        if Path("texput.log").exists():
            Path("texput.log").unlink()

        print("Galois LFSR diagram generated successfully:")
        for output in outputs:
            print(f"- {output}")

    except subprocess.CalledProcessError as e:
        print("Error during compilation/conversion:", file=sys.stderr)
        if "pdflatex" in str(e.cmd):
            print(
                "Failed to generate PDF. Check if pdflatex is installed.",
                file=sys.stderr,
            )
        elif "pdftops" in str(e.cmd):
            print(
                "Failed to generate EPS. Check if pdftops is installed.",
                file=sys.stderr,
            )
        elif "magick" in str(e.cmd):
            print(
                "Failed to generate PNG. Check if ImageMagick is installed.",
                file=sys.stderr,
            )
        sys.exit(1)


def main():
    import argparse
    import sys
    import warnings

    # Suppress syntax warnings about escape sequences
    warnings.filterwarnings("ignore", category=SyntaxWarning)

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="""Generate a Galois Linear Feedback Shift Register (LFSR) diagram.

A Galois LFSR is a specific type of LFSR where the feedback taps are XORed with
the output bit before being fed into the next register. This implementation is
more efficient in hardware compared to Fibonacci LFSRs.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--taps",
        type=parse_binary_list,
        help="Tap sequence as a string of 0s and 1s (rightmost is x_0)\n"
        "Default: 1001",
        default="1001",
    )
    parser.add_argument(
        "--init-values",
        type=parse_binary_list,
        help="Initial values as a string of 0s and 1s\n" "Default: 1111",
        default="1111",
    )
    parser.add_argument(
        "--hide-values",
        action="store_true",
        help="Hide values in the LFSR boxes (default: False)",
        default=False,
    )
    parser.add_argument(
        "--hide-names",
        action="store_true",
        help="Hide box names under the LFSR boxes (default: False)",
        default=False,
    )

    parser.add_argument(
        "--format",
        choices=["pdf", "png", "eps", "all"],
        help="Output format: pdf (default), png, eps, or all",
        default="pdf",
    )

    # Parse arguments, suppressing the default error output
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(1)

    # Validate input lengths match
    if len(args.taps) != len(args.init_values):
        print(
            "Error: Tap sequence and initial values must have the same length",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate input lengths are reasonable
    if len(args.taps) > 32:
        print("Error: LFSR length cannot exceed 32 bits", file=sys.stderr)
        sys.exit(1)

    # Print LFSR to file
    with open("lfsr.tex", "w") as f:
        # Redirect stdout to file
        original_stdout = sys.stdout
        sys.stdout = f

        # Generate LaTeX for Galois LFSR
        drawGaloisLFSR(args.taps, args.init_values, args.hide_values, args.hide_names)

        # Restore stdout
        sys.stdout = original_stdout

    # Compile and convert to requested format
    compile_and_convert(args.format)


if __name__ == "__main__":
    main()
