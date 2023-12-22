from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
import pandas as pd
import numpy as np

ligands = pd.read_csv('actvities.csv')

# radius=2, are roughly equivalent to ECFP4:
fpgen = AllChem.GetMorganGenerator(radius=2)
fps = []

for smile in ligands['canonical_smiles']:
    m = Chem.MolFromSmiles(smile)
    fp = fpgen.GetFingerprint(m)
    fps.append(fp)

# to calculate Tanimoto similarity
# similarity = DataStructs.TanimotoSimilarity(fps[0], fps[1])

# as bit vector:
# print(np.array(fps[0])) 
# indexes of nonzero values:
# print(np.nonzero(fps[0]))

# write as bit vectors: 0:2048 columns are bit representation, last column is molecule_chembl_id
df = pd.DataFrame(np.array(fps))
df['molecule_chembl_id'] = ligands['molecule_chembl_id']
df.to_csv('ligands_ecfp4.csv', index=False, header=True)
