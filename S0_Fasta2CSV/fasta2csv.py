#Convert .fa file to .csv file
#Input: input.fa
#Output: output.csv
import csv

def parse_fasta(file):
    """Parse a FASTA file and return a list of tuples (protein_id, sequence)."""
    with open(file, 'r') as f:
        protein_data = []
        protein_id = ""
        sequence = []
        
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if protein_id:
                    protein_data.append((protein_id, ''.join(sequence)))
                protein_id = line[1:].split()[0]  # Get the protein ID (remove '>')
                sequence = []  # Reset sequence for the new protein
            else:
                sequence.append(line)
        
        # Add the last protein
        if protein_id:
            protein_data.append((protein_id, ''.join(sequence)))
        
        return protein_data

def fasta_to_csv(fasta_file, csv_file):
    """Convert FASTA to CSV with two columns: Protein ID and Sequence."""
    protein_data = parse_fasta(fasta_file)
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Protein ID', 'Sequence'])  # Write header
        writer.writerows(protein_data)  # Write data

# Example usage:
fasta_file = 'input.fa'  # Replace with your input FASTA file
csv_file = 'output.csv'  # Replace with your desired output CSV file

fasta_to_csv(fasta_file, csv_file)
print(f"Converted {fasta_file} to {csv_file}")
