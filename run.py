from biomed_enriched import populate

# This call *overwrites* the Arrow dataset in-place so no extra disk space
# is required.  If you do want a separate output, pass `output_path`.
populate(
    dataset_path="/lustre/fsn1/projects/rech/rua/uvb79kr/rntc--pubmed-noncomm-sample",   # input Arrow dataset (will be mutated)
    xml_root="/lustre/fsn1/projects/rech/rua/uvb79kr/pubmed/pub/pmc/oa_bulk/oa_noncomm/xml",         # PMC dump root (read-only for most users)
    output_path="/lustre/fsn1/projects/rech/rua/uvb79kr/rntc--pubmed-noncomm-sample-populated",                            # DEFAULT: overwrite input dir
    num_proc=1,                                  # leverage Jean-Zay cores
)