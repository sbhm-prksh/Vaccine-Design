#Written by Shubham Prakash on 21/10/24
#This script will convert fasta file to csv.
#Fasta file name should be input.fa.
#Output will be a csv fill with two columns, protein ID and protein sequence named output.csv

import csv # so that we can open and write output in a csv
def parse_fasta(file):
    """Parse a FASTA file and return a list of tuples (protein_id, sequence)."""
    with open(file, 'r') as f:
        protein_data = [] # list to store the tuples of protein IDs and their sequences.
        protein_id = "" 
        sequence = []
        
        for line in f:
            line = line.strip() #it will remove whitespace from start or end.
            if line.startswith('>'):
                if protein_id: 
                    protein_data.append((protein_id, ''.join(sequence)))
                # Split by space and get the first word after '>'
                protein_id = line[1:].split()[0]  # Extract only the protein ID ignores rest of data of the header line
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
        writer.writerow(['Protein ID', 'Sequence'])  # Write name of the columnes
        writer.writerows(protein_data)  # Write each rows.

fasta_file = 'input.fa'  # INPUT FASTA File
csv_file = 'output.csv'  # OUTPUT CSV File
fasta_to_csv(fasta_file, csv_file)
print(f"Converted {fasta_file} to {csv_file}")
