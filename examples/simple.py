"""Minimal example using `populate` directly."""
from datasets import load_from_disk

from biomed_enriched import populate

DATASET_DIR = "/path/to/biomed-enriched"  # change to your dataset path
PMC_XML_ROOT = "/path/to/pmc/xml"  # change to your PMC XML dump
OUTPUT_DIR = "/path/to/populated-biomed-enriched" # remove for in-place

populate(DATASET_DIR, PMC_XML_ROOT, output_path=OUTPUT_DIR, splits="non-comm", num_proc=1)
print("✓ Dataset populated !")

ds = load_from_disk(OUTPUT_DIR)
print(ds["train"][0])
# ✓ Dataset enriched in-place
# {'article_id': '30343930', 'path': 'sec[0]/p[0]', 'text': 'El concepto de prescripción enfermera, en adelante PE, ha ido evolucionando a lo largo de los últimos años de la mano del desarrollo de la profesión enfermera, como un elemento relevante para su práctica asistencial. En la actualidad, a través de los estudios de grado, especialización y posgrado, se confiere una profesión enfermera con un elevado potencial y un desarrollo de su autonomía dentro del proceso asistencial. El concepto de PE surge a consecuencia de este crecimiento profesional, como un elemento de práctica avanzada y especialista, que forma parte del propio proceso enfermero y de su plan de cuidados 1 . El proceso enfermero se compone, en su estructura básica, de una valoración inicial para poder establecer el diagnóstico enfermero o determinar el problema de colaboración. A partir del diagnóstico o problemas de salud se establecerán el conjunto de intervenciones y acciones a realizar 2 .', 'id': '30343930_p0', 'section_title': 'Introducción', 'educational_score': 2.7421875, 'domain': 'biomedical', 'document_type': 'Other', 'domain_scores': [0.81591796875, 0.005252838134765625, 0.1785888671875], 'document_type_scores': [0.161865234375, 0.8349609375, 0.0023822784423828125, 0.0008230209350585938], 'authors': ['Sonia Fernández Molero', 'Iris Lumillo Gutiérrez', 'Alba Brugués Brugués', 'Andrés Baiget Ortega', 'Irene Cubells Asensio', 'Núria Fabrellas Padrés'], 'article_url': 'https://doi.org/10.1016/j.aprim.2018.06.006', 'license_type': 'CC BY-NC-ND', 'license_url': 'http://creativecommons.org/licenses/by-nc-nd/4.0/', 'language': 'es', 'language_score': 0.9999968990793373}