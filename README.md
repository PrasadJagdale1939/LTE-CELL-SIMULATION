# LTE Cell Simulation

This project simulates a 4G/LTE network cell with multiple users, resource blocks, and advanced scheduling algorithms (Proportional Fair, Round Robin, Max C/I). It models user mobility, shadow fading, and visualizes throughput distribution and evolution over time.

## Features

- **LTE cell coverage simulation**
- **User mobility and shadow fading**
- **Resource Block (RB) allocation**
- **Three scheduling algorithms:**  
  - Proportional Fair (PF)  
  - Round Robin (RR)  
  - Max Carrier-to-Interference (Max C/I)
- **Visualization:**  
  - User throughput distribution in the cell  
  - Throughput evolution over time

## Requirements

- Python 3.7+
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)

## Installation

1. **Clone the repository or download the script.**
2. **Install dependencies:**
    ```sh
    pip install numpy matplotlib
    ```

## Usage

1. **Edit the script**  
   Open `lte_cell_simulation.py` to adjust simulation parameters if needed (e.g., number of users, scheduling algorithm).

2. **Select scheduling algorithm**  
   At the top of the script, set:
   ```python
   scheduler = 'PF'  # Options: 'PF', 'RR', 'MaxCI'
   ```

3. **Run the simulation:**
    ```sh
    python lte_cell_simulation.py
    ```

4. **View results:**  
   - The script will display plots of user throughput distribution and throughput over time.
   - The terminal will show a summary table for the last time slot.

## Example Output

- **Cell plot:** Users are shown with color indicating their throughput.
- **Throughput over time:** Line plot for each user.
- **Terminal summary:** Table of CQI, RBs allocated, and throughput per user.

## Customization

- Change `num_users`, `num_rbs`, `num_slots`, or other parameters at the top of the script.
- Switch between scheduling algorithms by changing the `scheduler` variable.

## License

This project is for educational and research purposes.

---

**Author:**  
[Prasad Jagdale]# LTE-CELL-SIMULATION
