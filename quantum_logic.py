import numpy as np
from qiskit import QuantumCircuit
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
import warnings
warnings.filterwarnings('ignore')

class QuantumEnergyOptimizer:
    """
    Quantum optimizer using QAOA to select optimal renewable energy sites.
    """
    
    def __init__(self, n_sites_to_select=5, qaoa_layers=2):
        self.n_sites_to_select = n_sites_to_select
        self.qaoa_layers = qaoa_layers
        self.backend = AerSimulator()
        
    def create_qubo_matrix(self, suitability_scores, coordinates, risk_scores):
        """
        Create QUBO matrix for the optimization problem.
        
        Objective:
        - Maximize suitability scores
        - Penalize high-risk areas
        - Encourage geographic spread (decentralization)
        """
        n = len(suitability_scores)
        Q = np.zeros((n, n))
        
        # Diagonal terms: negative suitability (we minimize in QUBO)
        for i in range(n):
            # Reward high suitability
            Q[i, i] = -suitability_scores[i] * 100
            
            # Heavy penalty for high-risk areas (Risk_Score > 7)
            if risk_scores[i] > 7:
                Q[i, i] += 50  # Penalty
        
        # Off-diagonal terms: encourage geographic spread
        # Penalize selecting sites that are too close together
        for i in range(n):
            for j in range(i+1, n):
                # Calculate distance between sites
                lat_diff = coordinates[i][0] - coordinates[j][0]
                lon_diff = coordinates[i][1] - coordinates[j][1]
                distance = np.sqrt(lat_diff**2 + lon_diff**2)
                
                # Penalty if sites are too close (encourage spread)
                if distance < 0.05:  # ~5km threshold
                    Q[i, j] = 20  # Penalty for clustering
                else:
                    Q[i, j] = -5  # Small reward for distributed sites
        
        # Add constraint penalty: must select exactly N sites
        penalty = 200
        for i in range(n):
            Q[i, i] += penalty * (1 - 2 * self.n_sites_to_select)
            for j in range(i+1, n):
                Q[i, j] += 2 * penalty
        
        return Q
    
    def qubo_to_ising(self, Q):
        """
        Convert QUBO to Ising Hamiltonian for QAOA.
        """
        n = Q.shape[0]
        h = np.zeros(n)
        J = np.zeros((n, n))
        offset = 0
        
        # Convert QUBO to Ising
        for i in range(n):
            h[i] = Q[i, i] / 2
            offset += Q[i, i] / 4
            for j in range(i+1, n):
                J[i, j] = Q[i, j] / 4
                h[i] += Q[i, j] / 4
                h[j] += Q[i, j] / 4
                offset += Q[i, j] / 4
        
        return h, J, offset
    
    def create_hamiltonian(self, h, J):
        """
        Create Hamiltonian operator from Ising parameters.
        """
        n = len(h)
        pauli_list = []
        coeffs = []
        
        # Single qubit terms
        for i in range(n):
            if abs(h[i]) > 1e-10:
                pauli_str = ['I'] * n
                pauli_str[i] = 'Z'
                pauli_list.append(''.join(pauli_str))
                coeffs.append(h[i])
        
        # Two qubit terms
        for i in range(n):
            for j in range(i+1, n):
                if abs(J[i, j]) > 1e-10:
                    pauli_str = ['I'] * n
                    pauli_str[i] = 'Z'
                    pauli_str[j] = 'Z'
                    pauli_list.append(''.join(pauli_str))
                    coeffs.append(J[i, j])
        
        if not pauli_list:
            pauli_list = ['I' * n]
            coeffs = [0.0]
        
        return SparsePauliOp(pauli_list, coeffs=coeffs)
    
    def optimize(self, suitability_scores, coordinates, risk_scores, progress_callback=None):
        """
        Run QAOA optimization to select optimal sites.
        
        Returns:
            selected_indices: List of indices of selected sites
            energy: Final energy value
        """
        n = len(suitability_scores)
        
        if progress_callback:
            progress_callback("Creating QUBO matrix...")
        
        # Create QUBO matrix
        Q = self.create_qubo_matrix(suitability_scores, coordinates, risk_scores)
        
        if progress_callback:
            progress_callback("Converting to Ising Hamiltonian...")
        
        # Convert to Ising
        h, J, offset = self.qubo_to_ising(Q)
        
        # Create Hamiltonian
        hamiltonian = self.create_hamiltonian(h, J)
        
        if progress_callback:
            progress_callback(f"Running QAOA with {self.qaoa_layers} layers...")
        
        try:
            # Setup QAOA
            sampler = StatevectorSampler()
            optimizer = COBYLA(maxiter=100)
            
            qaoa = QAOA(
                sampler=sampler,
                optimizer=optimizer,
                reps=self.qaoa_layers,
                initial_point=None
            )
            
            # Run optimization
            result = qaoa.compute_minimum_eigenvalue(hamiltonian)
            
            if progress_callback:
                progress_callback("Processing quantum results...")
            
            # Extract best solution
            eigenstate = result.eigenstate
            
            # Get the most probable bitstring
            if hasattr(eigenstate, 'binary_probabilities'):
                probs = eigenstate.binary_probabilities()
                best_bitstring = max(probs.items(), key=lambda x: x[1])[0]
            else:
                # Fallback: measure the quantum state
                best_bitstring = self._measure_state(result, n)
            
            # Convert bitstring to list of selected indices
            selected = [i for i, bit in enumerate(best_bitstring) if bit == '1']
            
            # If we don't have exactly N sites, use greedy selection
            if len(selected) != self.n_sites_to_select:
                if progress_callback:
                    progress_callback(f"Adjusting selection to exactly {self.n_sites_to_select} sites...")
                selected = self._greedy_selection(suitability_scores, risk_scores, n)
            
            energy = result.eigenvalue.real + offset
            
            if progress_callback:
                progress_callback("✅ Optimization complete!")
            
            return selected, energy
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"⚠️ QAOA failed, using greedy fallback: {str(e)}")
            
            # Fallback to greedy selection
            selected = self._greedy_selection(suitability_scores, risk_scores, n)
            return selected, 0.0
    
    def _measure_state(self, result, n):
        """
        Measure quantum state to get bitstring.
        """
        # Simple measurement simulation
        eigenstate = result.eigenstate
        probabilities = np.abs(eigenstate.data) ** 2
        
        # Get most probable state
        max_idx = np.argmax(probabilities)
        bitstring = format(max_idx, f'0{n}b')
        
        return bitstring
    
    def _greedy_selection(self, suitability_scores, risk_scores, n):
        """
        Greedy fallback: select top N sites by suitability, avoiding high-risk areas.
        """
        # Penalize high-risk sites
        adjusted_scores = suitability_scores.copy()
        for i in range(n):
            if risk_scores[i] > 7:
                adjusted_scores[i] *= 0.3  # Heavy penalty
        
        # Select top N
        selected_indices = np.argsort(adjusted_scores)[-self.n_sites_to_select:]
        return selected_indices.tolist()
