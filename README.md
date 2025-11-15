# TransportationLPSolver

TransportationLPSolver is a Python desktop application for solving the **Transportation Problem** in Linear Programming using the **Potentials Method (U-V algorithm)**. It features a modern GUI built with **PyQt5**, and supports various solving methods including **Vogel's Approximation Method**.

## Features

* 🧠 Implements both the Potentials (U-V) Method and Vogel's Approximation Method
* 🖥️ Intuitive PyQt-based graphical user interface
* ⚡ Fast matrix manipulation and computation with NumPy
* 📊 Real-time display of results and steps
* 🧪 Comprehensive unit tests included for core algorithms
* 📁 Modular project structure and reusable components

## Project Structure

```
TransportationLPSolver
├── main.py                    # Entry point for the application
├── core/                      # Core algorithms for solving transportation problems
│   ├── potential_method.py
│   ├── tlp_solver.py
│   └── vogels_method.py
├── utils/                     # Helper utilities and classes
│   ├── containers.py
│   ├── formatters.py
│   ├── validators.py
│   └── ...
├── view/                      # PyQt UI components
│   ├── app_window.py
│   ├── input_widget.py
│   └── result_widget.py
├── tests/                     # Unit tests for solver logic
│   ├── test_potential.py
│   └── test_vogel.py
├── docs/                      # Optional documentation folder
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/TransportationLPSolver.git
   cd TransportationLPSolver
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application from the command line:

```bash
python main.py
```

After launching, the GUI allows you to:

* Enter supply/demand and cost matrix
* Choose the solving method (Vogel or Potentials)
* View the solution and steps interactively

## Running Tests

To run unit tests (requires `pytest`):

```bash
pytest
```

## Requirements

* Python 3.8+
* PyQt5
* NumPy
* pytest (for testing)

Install all Python dependencies via the included `requirements.txt` file.
