#Written by Shubham Prakash on 22/10/24
#Purpose: This script will convert fasta file to csv.
#Input: A fasta file. Update fasta_file variable according to your input.
#Output: A CSV file. Update csv_file variable to whaterver name you wants.
import pandas as pd

def parse_fasta(file):
    """Parse a FASTA file and return a dictionary with protein IDs and sequences."""
    # Initialize the dictionary to hold your data
    data = {
        'Protein ID': [],
        'Sequence': [],
        'Allergen Test':[],
        'Antigen Test':[],
        'Signal P':[]
    }
    
    with open(file, 'r') as f:
        protein_id = ""
        sequence = []  # Will store all lines of a sequence
        
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if protein_id:
                    # Append the protein ID and sequence to the dictionary
                    data['Protein ID'].append(protein_id)
                    data['Sequence'].append(''.join(sequence))
                    data['Allergen Test'].append("Pending")
                    data['Antigen Test'].append("Pending")
                    data['Signal P'].append("Pending")
                protein_id = line[1:].split()[0]  # Get the protein ID
                sequence = []  # Reset sequence
            else:
                sequence.append(line)
        
        # Add the last protein
        if protein_id:
            data['Protein ID'].append(protein_id)
            data['Sequence'].append(''.join(sequence))
            data['Allergen Test'].append("Pending")
            data['Antigen Test'].append("Pending")
            data['Signal P'].append("Pending")
    
    return data

def fasta_to_csv(fasta_file, csv_file):
    """Convert FASTA to CSV using pandas."""
    data = parse_fasta(fasta_file)
    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)  # Write DataFrame to CSV

fasta_file = 'smallInput.fa'  # INPUT FASTA File
csv_file = 'smalloutput.csv'  # OUTPUT CSV File
fasta_to_csv(fasta_file, csv_file)
print(f"Success: Converted {fasta_file}->{csv_file}")
