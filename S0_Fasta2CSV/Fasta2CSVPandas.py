#Same task as fasta2csv.py but using pandas
#Written by Shubham Prakash on 22/10/24
#This script will convert fasta file to csv.
#Fasta file name should be input.fa.
#Output will be a csv fill with two columns, protein ID and protein sequence named output.csv
import pandas as pd

def parse_fasta(file):
    """Parse a FASTA file and return a DataFrame with protein IDs and sequences."""
    protein_data = []
    with open(file, 'r') as f:
        protein_id = ""
        sequence = [] #will store all the lines of A sequence
        
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if protein_id:
                    protein_data.append((protein_id, ''.join(sequence)))
                protein_id = line[1:].split()[0]  # Get the protein ID
                sequence = []  # Reset sequence
            else:
                sequence.append(line)
        
        # Add the last protein
        if protein_id:
            protein_data.append((protein_id, ''.join(sequence)))
    
    return pd.DataFrame(protein_data, columns=['Protein ID', 'Sequence'])

def fasta_to_csv(fasta_file, csv_file):
    """Convert FASTA to CSV using pandas."""
    df = parse_fasta(fasta_file)
    df.to_csv(csv_file, index=False)  # Write DataFrame to CSV

fasta_file = 'input.fa'  # INPUT FASTA File
csv_file = 'output.csv'  # OUTPUT CSV File
fasta_to_csv(fasta_file, csv_file)
print(f"Converted {fasta_file} to {csv_file}")
