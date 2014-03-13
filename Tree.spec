/*
Phylogenetic Tree and Multiple Sequence Alignment Services

This service provides a set of methods for querying, manipulating, and analyzing multiple
sequence alignments and phylogenetic trees.

Authors
---------
Michael Sneddon, LBL (mwsneddon@lbl.gov)
Fangfang Xia, ANL (fangfang.xia@gmail.com)
Keith Keller, LBL (kkeller@lbl.gov)
Matt Henderson, LBL (mhenderson@lbl.gov)
Dylan Chivian, LBL (dcchivian@lbl.gov)

*/
module Tree
{
    /* *********************************************************************************************** */
    /* ALIGNMENT AND TREE DATA TYPES */
    /* *********************************************************************************************** */

    /* indicates true or false values, false <= 0, true >=1 */
    typedef int boolean;
    
    /* time in units of number of seconds since the epoch */
    typedef string timestamp;
    
    /* integer number indicating a 1-based position in an amino acid / nucleotide sequence */
    typedef int position;
    
    /* A KBase ID is a string starting with the characters "kb|".  KBase IDs are typed. The types are
    designated using a short string. For instance," g" denotes a genome, "tree" denotes a Tree, and
    "aln" denotes a sequence alignment. KBase IDs may be hierarchical.  For example, if a KBase genome
    identifier is "kb|g.1234", a protein encoding gene within that genome may be represented as
    "kb|g.1234.peg.771".
    */
    typedef string kbase_id;

    /* A string representation of a phylogenetic tree.  The format/syntax of the string is
    specified by using one of the available typedefs declaring a particular format, such as 'newick_tree',
    'phylo_xml_tree' or 'json_tree'.  When a format is not explictily specified, it is possible to return
    trees in different formats depending on addtional parameters. Regardless of format, all leaf nodes
    in trees built from MSAs are indexed to a specific MSA row.  You can use the appropriate functionality
    of the API to replace these IDs with other KBase Ids instead. Internal nodes may or may not be named.
    Nodes, depending on the format, may also be annotated with structured data such as bootstrap values and
    distances.
    */
    typedef string tree;

    /* Trees are represented in KBase by default in newick format (http://en.wikipedia.org/wiki/Newick_format)
    and are returned to you in this format by default.  
    */
    typedef tree newick_tree;
    
    /* Trees are represented in KBase by default in newick format (http://en.wikipedia.org/wiki/Newick_format),
    but can optionally be converted to the more verbose phyloXML format, which is useful for compatibility or
    when additional information/annotations decorate the tree.
    */
    typedef tree phylo_xml_tree;
    
    /* Trees are represented in KBase by default in newick format (http://en.wikipedia.org/wiki/Newick_format),
    but can optionally be converted to JSON format where the structure of the tree matches the structure of
    the JSON object.  This is useful when interacting with the tree in JavaScript, for instance. 
    */
    typedef tree json_tree;
    
    /* String representation of a sequence alignment, the format of which may be different depending on
    input options for retrieving the alignment.
    */
    typedef string alignment;
    
    
    /* String representation of a sequence or set of sequences in FASTA format.  The precise alphabet used is
    not yet specified, but will be similar to sequences stored in KBase with '-' to denote gaps in alignments.
    */
    typedef string fasta;
    
    /* String representation of an alignment in FASTA format.  The precise alphabet and syntax of the alignment
    string is not yet specified, but will be similar to sequences stored in KBase  with '-' to denote gaps in
    alignments.
    */
    typedef fasta fasta_alignment;
    
    /* The string representation of the parsed node name (may be a kbase_id, but does not have to be).  Note that this
    is not the full, raw label in a newick_tree (which may include comments).
    */
    typedef string node_name;
    
    /* String in HTML format, used in the KBase Tree library for returning rendered trees. */
    typedef string html_file;
    


    /* A convenience type representing a genome id reference. This might be a kbase_id (in the case of 
    a CDM genome) or, more likely, a workspace reference of the structure "ws/obj/ver"
    */
    typedef string genome_ref;

    /* A string representation of the scientific name of a species.
    */
    typedef string scientific_name;

    /* A tuple that gives very basic information about a single genome in a SpeciesTree - enough to decorate 
    the nodes with the species name, and fetch more genome information from the KBase datastores.
    */
    typedef tuple<genome_ref ref, scientific_name name> genome_info;

    /* The structure of a tree itself.

        tree - the Newick string representing the tree itself
        id_map - maps from internal tree node ids to workspace references for each genome
        alignment_ref - (optional) the reference to the alignment from which the tree was built
    */
    typedef structure {
        newick_tree species_tree;
        mapping<node_name, genome_info> id_map;
        string alignment_ref;
    } SpeciesTree;


    
    /* Meta data associated with a tree.
    
        kbase_id alignment_id - if this tree was built from an alignment, this provides that alignment id
        string type - the type of tree; possible values currently are "sequence_alignment" and "genome" for trees
                      either built from a sequence alignment, or imported directly indexed to genomes.
        string status - set to 'active' if this is the latest built tree for a particular gene family
        timestamp date_created - time at which the tree was built/loaded in seconds since the epoch
        string tree_contruction_method - the name of the software used to construct the tree
        string tree_construction_parameters - any non-default parameters of the tree construction method
        string tree_protocol - simple free-form text which may provide additional details of how the tree was built
        int node_count - total number of nodes in the tree
        int leaf_count - total number of leaf nodes in the tree (generally this cooresponds to the number of sequences)
        string source_db - the source database where this tree originated, if one exists
        string source_id - the id of this tree in an external database, if one exists 
    */
    typedef structure {
        kbase_id alignment_id;
        string type;
        string status;
        timestamp date_created;
        string tree_contruction_method;
        string tree_construction_parameters;
        string tree_protocol;
        int node_count;
        int leaf_count;
        string source_db;
        string source_id;
    } TreeMetaData;
    
    
    /* Meta data associated with an alignment.
    
        list<kbase_id> tree_ids - the set of trees that were built from this alignment
        string status - set to 'active' if this is the latest alignment for a particular set of sequences
        string sequence_type - indicates what type of sequence is aligned (e.g. protein vs. dna)
        boolean is_concatenation - true if the alignment is based on the concatenation of multiple non-contiguous
                                sequences, false if each row cooresponds to exactly one sequence (possibly with gaps)
        timestamp date_created - time at which the alignment was built/loaded in seconds since the epoch
        int n_rows - number of rows in the alignment
        int n_cols - number of columns in the alignment
        string alignment_construction_method - the name of the software tool used to build the alignment
        string alignment_construction_parameters - set of non-default parameters used to construct the alignment
        string alignment_protocol - simple free-form text which may provide additional details of how the alignment was built
        string source_db - the source database where this alignment originated, if one exists
        string source_id - the id of this alignment in an external database, if one exists
    */
    typedef structure {
        list<kbase_id> tree_ids;
        string status;
        string sequence_type;
        string is_concatenation;
        timestamp date_created;
        int n_rows;
        int n_cols;
        string alignment_construction_method;
        string alignment_construction_parameters;
        string alignment_protocol;
        string source_db;
        string source_id;
    } AlignmentMetaData;
    
    
    
    /*
    These structures are not currently used yet, and are therefore commented out....
    
    typedef structure {
        int beg_pos_aln;
        int end_pos_aln;
        int beg_pos_in_parent;
        int end_pos_in_parent;
        int parent_seq_length;
        string md5_of_ungapped_sequence;
        
        string parent_sequence;
        string parent_sequence_type;
        string parent_sequence_md5;
        
        string parent_sequence_canonical_kb_feature_id;
    
    } AlignmentRowComponent;
    
    typedef structure {
        string row_id;
        string row_description;
        string raw_row_sequence;
        list <AlignmentRowComponent> components;
    } AlignmentRow;
    
    typedef structure {
        string alignment_id;
        list<AlignmentRow> rows;
        mapping<string,string> alignment_attributes;
        string status;
        boolean is_concatenation
        string sequence_type
        timestamp timestamp
        string method
        string parameters
        string protocol;
        string source_db;
        string source_id;
    } Alignment;
    
    typedef structure {
        string tree_id;
        newick_tree newick_tree;
        mapping<string,string> tree_attributes;
        mapping<string,mapping<string,string>> node_attributes;
        string status;
        string data_type;
        timestamp timestamp;
        string method;
        string parameters;
        string protocol;
        string source_id;
        string source_db;
    } Tree;
    
    
    typedef structure {
        Tree tree;
        Alignment alignment;
    } AlignmentTree;
    */
    
    
    
    /* *********************************************************************************************** */
    /* METHODS FOR TREE PARSING AND STRING MANIPULATIONS */
    /* *********************************************************************************************** */

    /* Given a tree in newick format, replace the node names indicated as keys in the 'replacements' mapping
    with new node names indicated as values in the 'replacements' mapping.  Matching is EXACT and will not handle
    regular expression patterns.
    */
    funcdef replace_node_names(newick_tree tree, mapping<node_name,node_name>replacements) returns (newick_tree);
    
    /* Given a tree in newick format, remove the nodes with the given names indicated in the list, and
    simplify the tree.  Simplifying a tree involves removing unnamed internal nodes that have only one
    child, and removing unnamed leaf nodes.  During the removal process, edge lengths (if they exist) are
    conserved so that the summed end to end distance between any two nodes left in the tree will remain the same.
    */
    funcdef remove_node_names_and_simplify(newick_tree tree, list<node_name>removal_list) returns (newick_tree);
   
    /* Some KBase trees keep information on canonical feature ids, even if they have the same protien sequence
    in an alignment.  In these cases, some leaves with identical sequences will have zero distance so that
    information on canonical features is maintained.  Often this information is not useful, and a single
    example feature or genome is sufficient.  This method will accept a tree in newick format (with distances)
    and merge all leaves that have zero distance between them (due to identical sequences), and keep arbitrarily
    only one of these leaves.
    */
    funcdef merge_zero_distance_leaves(newick_tree tree) returns (newick_tree);
   
   
    /* NOTE: methods that are commented out are not yet fully implemented yet, but will likely appear in future
    versions of the Tree service as they are needed or requested.*/
    /* Convert a tree encoded in newick format to a tree encded in phyloXML format.
    */
    /* funcdef convert_newick2phyloXML(newick_tree tree) returns (phylo_xml_tree); */
    /* Convert a tree encoded in newick format to a tree encded in phyloXML format.
    */
    /* funcdef convert_phyloXML2newick(newick_tree tree) returns (phylo_xml_tree); */
    /* Convert a tree encoded in newick format to a tree encded in JSON format.
    */
    /* funcdef convert_newick2json(newick_tree tree) returns (json_tree); */
    /* Convert a tree encoded in JSON format to a tree encded in newick format.
    */
    /* funcdef convert_json2newick(json_tree tree) returns (newick_tree); */
    
    

    
    
    
    /* *********************************************************************************************** */
    /* METHODS FOR TREE INTROSPECTION */
    /* These are methods that make a tree tell you about itself.  These methods operate on any newick  */
    /* tree that is passed in, and requires no direct connecion to the CDM.                            */
    /* *********************************************************************************************** */
  
    /* Given a tree in newick format, list the names of the leaf nodes.
    */
    funcdef extract_leaf_node_names(newick_tree tree) returns (list<node_name>);
    
    /* Given a tree in newick format, list the names of ALL the nodes.  Note that for some trees, such as
    those originating from MicrobesOnline, the names of internal nodes may be bootstrap values, but will still
    be returned by this function.
    */
    funcdef extract_node_names(newick_tree tree) returns (list<node_name>);
    
    /* Given a tree, return the total number of nodes, including internal nodes and the root node.
    */
    funcdef get_node_count(newick_tree tree) returns (int);
    
    /* Given a tree, return the total number of leaf nodes, (internal and root nodes are ignored).  When the
    tree was based on a multiple sequence alignment, the number of leaves will match the number of sequences
    that were aligned.
    */
    funcdef get_leaf_count(newick_tree tree) returns (int);
    
    
    
    
    
    /* *********************************************************************************************** */
    /* METHODS FOR ALIGNMENT AND TREE RETRIEVAL */
    /* *********************************************************************************************** */
    
    /* Returns the specified tree in the specified format, or an empty string if the tree does not exist.
    The options hash provides a way to return the tree with different labels replaced or with different attached meta
    information.  Currently, the available flags and understood options are listed below. 
    
        options = [
            format => 'newick',
            newick_label => 'none' || 'raw' || 'feature_id' || 'protein_sequence_id' ||
                            'contig_sequence_id' || 'best_feature_id' || 'best_genome_id',
            newick_bootstrap => 'none' || 'internal_node_labels'
            newick_distance => 'none' || 'raw'
        ];
 
    The 'format' key indicates what string format the tree should be returned in.  Currently, there is only
    support for 'newick'. The default value if not specified is 'newick'.
    
    The 'newick_label' key only affects trees returned as newick format, and specifies what should be
    placed in the label of each leaf.  'none' indicates that no label is added, so you get the structure
    of the tree only.  'raw' indicates that the raw label mapping the leaf to an alignement row is used.
    'feature_id' indicates that the label will have an examplar feature_id in each label (typically the
    feature that was originally used to define the sequence). Note that exemplar feature_ids are not
    defined for all trees, so this may result in an empty tree! 'protein_sequence_id' indicates that the
    kbase id of the protein sequence used in the alignment is used.  'contig_sequence_id' indicates that
    the contig sequence id is added.  Note that trees are typically built with protein sequences OR
    contig sequences. If you select one type of sequence, but the tree was built with the other type, then
    no labels will be added.  'best_feature_id' is used in the frequent case where a protein sequence has
    been mapped to multiple feature ids, and an example feature_id is used.  Similarly, 'best_genome_id'
    replaces the labels with the best example genome_id.  The default value if none is specified is 'raw'.
    
    The 'newick_bootstrap' key allows control over whether bootstrap values are returned if they exist, and
    how they are returned.  'none' indicates that no bootstrap values are returned. 'internal_node_labels'
    indicates that bootstrap values are returned as internal node labels.  Default value is 'internal_node_labels';
    
    The 'newick_distance' key allows control over whether distance labels are generated or not.  If set to
    'none', no distances will be output. Default is 'raw', which outputs the distances exactly as they appeared
    when loaded into KBase.
    */
    funcdef get_tree(kbase_id tree_id, mapping<string,string> options) returns (tree);
    
    
    
    
    
    /* Returns the specified alignment in the specified format, or an empty string if the alignment does not exist.
    The options hash provides a way to return the alignment with different labels replaced or with different attached meta
    information.  Currently, the available flags and understood options are listed below. 
    
        options = [
            format => 'fasta',
            sequence_label => 'none' || 'raw' || 'feature_id' || 'protein_sequence_id' || 'contig_sequence_id',
        ];
 
    The 'format' key indicates what string format the alignment should be returned in.  Currently, there is only
    support for 'fasta'. The default value if not specified is 'fasta'.
    
    The 'sequence_label' specifies what should be placed in the label of each sequence.  'none' indicates that
    no label is added, so you get the sequence only.  'raw' indicates that the raw label of the alignement row
    is used. 'feature_id' indicates that the label will have an examplar feature_id in each label (typically the
    feature that was originally used to define the sequence). Note that exemplar feature_ids are not
    defined for all alignments, so this may result in an unlabeled alignment.  'protein_sequence_id' indicates
    that the kbase id of the protein sequence used in the alignment is used.  'contig_sequence_id' indicates that
    the contig sequence id is used.  Note that trees are typically built with protein sequences OR
    contig sequences. If you select one type of sequence, but the alignment was built with the other type, then
    no labels will be added.  The default value if none is specified is 'raw'.
    */
    funcdef get_alignment(kbase_id alignment_id, mapping<string,string> options) returns (alignment);

    /* Get meta data associated with each of the trees indicated in the list by tree id.  Note that some meta
    data may not be available for trees which are not built from alignments.  Also note that this method
    computes the number of nodes and leaves for each tree, so may be slow for very large trees or very long
    lists.  If you do not need this full meta information structure, it may be faster to directly query the
    CDS for just the field you need using the CDMI.
    */
    funcdef get_tree_data(list<kbase_id> tree_ids) returns (mapping<kbase_id,TreeMetaData>);
    
    /* Get meta data associated with each of the trees indicated in the list by tree id.  Note that some meta
    data may not be available for trees which are not built from alignments.  Also note that this method
    computes the number of nodes and leaves for each tree, so may be slow for very large trees or very long
    lists.  If you do not need this full meta information structure, it may be faster to directly query the
    CDS for just the field you need using the CDMI.
    */
    funcdef get_alignment_data(list<kbase_id> alignment_ids) returns (mapping<kbase_id,AlignmentMetaData>);
    
    /* Given a list of feature ids in kbase, the protein sequence of each feature (if the sequence exists)
    is identified and used to retrieve all trees by ID that were built using the given protein sequence. */
    funcdef get_tree_ids_by_feature(list <kbase_id> feature_ids) returns (list<kbase_id>);
    
    /* Given a list of kbase ids of a protein sequences (their MD5s), retrieve the tree ids of trees that
    were built based on these sequences. */
    funcdef get_tree_ids_by_protein_sequence(list <kbase_id> protein_sequence_ids) returns (list<kbase_id>);
    
    /* Given a list of feature ids in kbase, the protein sequence of each feature (if the sequence exists)
    is identified and used to retrieve all alignments by ID that were built using the given protein sequence.*/
    funcdef get_alignment_ids_by_feature(list <kbase_id> feature_ids) returns (list<kbase_id>);
    
    /* Given a list of kbase ids of a protein sequences (their MD5s), retrieve the alignment ids of trees that
    were built based on these sequences. */
    funcdef get_alignment_ids_by_protein_sequence(list <kbase_id> protein_sequence_ids) returns (list<kbase_id>);
  
    /* This method searches for a tree having a source ID that matches the input pattern.  This method accepts
    one argument, which is the pattern.  The pattern is very simple and includes only two special characters,
    wildcard character, '*', and a match-once character, '.'  The wildcard character matches any number (including
    0) of any character, the '.' matches exactly one of any character.  These special characters can be escaped
    with a backslash.  To match a blackslash literally, you must also escape it.  Note that source IDs are
    generally defined by the gene family model which was used to identifiy the sequences to be included in
    the tree.  Therefore, matching a source ID is a convenient way to find trees for a specific set of gene
    families. */
    funcdef get_tree_ids_by_source_id_pattern(string pattern) returns (list<list<kbase_id>>);
    
    
    /* Given a tree id, this method returns a mapping from a tree's unique internal ID to
    a protein sequence ID. */
    funcdef get_leaf_to_protein_map(kbase_id tree_id) returns (mapping<kbase_id,kbase_id>);
    
    /* Given a tree id, this method returns a mapping from a tree's unique internal ID to
    a KBase feature ID if and only if a cannonical feature id exists. */
    funcdef get_leaf_to_feature_map(kbase_id tree_id) returns (mapping<kbase_id,kbase_id>);
    
    
    /* Returns all tree IDs in which the entire portion of the given sequence (which can optionally
    include start and end positions of the sequence) is used in the alignment which generates the tree.
    todo: should beg/end just be included in some options hash?
    todo: define contents of options hash, which will allow more complex queries, such as returning
          only active trees, or trees of a particuar hieght, etc...
    funcdef get_trees_with_entire_seq(fasta sequence, position beg, position end, mapping<string,string> options) returns (list<kbase_id>);
    */
    
    /* Returns all tree IDs in which some portion of the given sequence (which can optionally
    include start and end positions of the sequence) is used in the alignment which generates the tree.
    funcdef get_trees_with_overlapping_seq(fasta sequence, position beg, position end, mapping<string,string> options) returns (list<kbase_id>);
    */
    
    /* Returns all tree IDs in which the entire portion of the given domain is used in the alignment
    which generates the tree (usually the tree will be constructed based on this domain). NOT FUNCTIONAL UNTIL KBASE HAS HOMOLOGUE/DOMAIN LOOKUPS
    funcdef get_trees_with_entire_domain(kbase_id domain, mapping<string,string>options) returns (list<kbase_id>);
    */
    
    /* Returns all tree IDs in which some portion of the given domain is used in the alignment
    which generates the tree (usually such trees will be constructed based on a similar domain created
    with an alternative method, so the entire domain may not be contained).  NOT FUNCTIONAL UNTIL KBASE HAS HOMOLOGUE/DOMAIN LOOKUPS
    funcdef get_trees_with_overlapping_domain(kbase_id domain, mapping<string,string>options) returns (list<kbase_id>);
    */
    


    /* *********************************************************************************************** */
    /* METHODS FOR TREE-BASED METAGENOMIC ANALYSIS */
    /* *********************************************************************************************** */

    /* Structure to group input parameters to the compute_abundance_profile method.
    
        kbase_id tree_id                - the KBase ID of the tree to compute abundances for; the tree is
                                          used to identify the set of sequences that were aligned to build
                                          the tree; each leaf node of a tree built from an alignment will
                                          be mapped to a sequence; the compute_abundance_profile method
                                          assumes that trees are built from protein sequences
        string protein_family_name      - the name of the protein family used to pull a small set of reads
                                          from a metagenomic sample; currently only COG families are supported
        string protein_family_source    - the name of the source of the protein family; currently supported
                                          protein families are: 'COG'
        string metagenomic_sample_id    - the ID of the metagenomic sample to lookup; see the KBase communities
                                          service to identifiy metagenomic samples
        int percent_identity_threshold  - the minimum acceptable percent identity for hits, provided as a percentage
                                          and not a fraction (i.e. set to 87.5 for 87.5%)
        int match_length_threshold      - the minimum acceptable length of a match to consider a hit
    */
    typedef structure {
        kbase_id tree_id;
        string protein_family_name;
        string protein_family_source;
        string metagenomic_sample_id;
        int percent_identity_threshold;
        int match_length_threshold;
        string mg_auth_key;
    } AbundanceParams;
    
    /* Structure to group output of the compute_abundance_profile method.
    
        mapping <string,int> abundances - maps the raw row ID of each leaf node in the input tree to the number
                                          of hits that map to the given leaf; only row IDs with 1 or more hits
                                          are added to this map, thus missing leaf nodes imply 0 hits
        int n_hits                      - the total number of hits in this sample to any leaf
        int n_reads                     - the total number of reads that were identified for the input protein
                                          family; if the protein family could not be found this will be zero.
    */
    typedef structure {
        mapping <string,int> abundances;
        int n_hits;
        int n_reads;
    } AbundanceResult;
    
    /*
    Given an input KBase tree built from a sequence alignment, a metagenomic sample, and a protein family, this method
    will tabulate the number of reads that match to every leaf of the input tree.  First, a set of assembled reads from
    a metagenomic sample are pulled from the KBase communities service which have been determined to be a likely hit
    to the specified protein family.  Second, the sequences aligned to generate the tree are retrieved.  Third, UCLUST [1]
    is used to map reads to target sequences of the tree.  Finally, for each leaf in the tree, the number of hits matching
    the input search criteria is tabulated and returned.  See the defined objects 'abundance_params' and 'abundance_result'
    for additional details on specifying the input parameters and handling the results.
    
    [1] Edgar, R.C. (2010) Search and clustering orders of magnitude faster than BLAST, Bioinformatics 26(19), 2460-2461.
    */
    funcdef compute_abundance_profile(AbundanceParams abundance_params) returns (AbundanceResult abundance_result);


    /* map an id to a number (e.g. feature_id mapped to a log2 normalized abundance value) */
    typedef mapping<string,float> abundance_profile;

    /* map the name of the profile with the profile data */
    typedef mapping <string, abundance_profile> abundance_data;

    
    /*
      cutoff_value                  => def: 0 || [any_valid_float_value]
      use_cutoff_value              => def: 0 || 1
      normalization_scope           => def:'per_column' || 'global'
      normalization_type            => def:'none' || 'total' || 'mean' || 'max' || 'min'
      normalization_post_process    => def:'none' || 'log10' || 'log2' || 'ln'
    */
    typedef structure {
        float cutoff_value;
        boolean use_cutoff_value;
        float cutoff_number_of_records;
        boolean use_cutoff_number_of_records;
        string normalization_scope;
        string normalization_type;
        string normalization_post_process;
    } FilterParams;

    /* 
    ORDER OF OPERATIONS:
    1) using normalization scope, defines whether process should occur per column or globally over every column
    2) using normalization type, normalize by dividing values by the option indicated
    3) apply normalization post process if set (ie take log of the result)
    4) apply the cutoff_value threshold to all records, eliminating any that are not above the specified threshold
    5) apply the cutoff_number_of_records (always applies per_column!!!), discarding any record that are not in the top N record values for that column
    
    - if a value is not a valid number, it is ignored
    
    */
    funcdef filter_abundance_profile(abundance_data abundance_data, FilterParams filter_params) returns (abundance_data abundance_data_processed);
    
    
    
    /* *********************************************************************************************** */
    /* METHODS FOR TREE-BASED FEATURE/SEQUENCE LOOKUPS */
    /* *********************************************************************************************** */
 
    /*
    Given a list of kbase identifiers for a tree, substitutes the leaf node labels with actual kbase sequence
    identifiers.  If a particular alignment row maps to a single sequence, this is straightforward.  If an
    alignmnt row maps to multiple sequences, then the current behavior is not yet defined (likely will be
    a concatenated list of sequence ids that compose the alignment row).  Options Hash allows addiional
    parameters to be passed (parameter list is also currently not defined yet and is currently ignored.)
    */
    /*funcdef substitute_node_names_with_kbase_ids(list <kbase_id> trees, mapping<string,string> options) returns (list<newick_tree>);*/

 
    /* Given an alignment and a row in the alignment, returns all the kbase_ids of the sequences that compose
    the given tree. Note: may not be needed if this functionality is possible via the ER model.
    NOTE: currently not needed because there are no alignments built from concatenated sequences yet...
    */
    /* funcdef get_kbase_ids_from_alignment_row(kbase_id alignment_id, int row_number) returns (list<kbase_id>); */

 
 
    /* *********************************************************************************************** */
    /* METHODS FOR TREE RESTRUCTURING */
    /* *********************************************************************************************** */
 
    /* Given a tree in KBASE and a sequence in FASTA format, attempt to add the new sequence into the tree.  This
    method requires that the tree was built from a multiple sequence alignment and that the tree/alignment is stored
    in KBASE.  This method returns
    */
    /* funcdef add_node_to_tree(kbase_id tree_id, kbase_id sequence_id, mapping<string,string> options) returns (newick_tree); */

 
    /* *********************************************************************************************** */
    /* METHODS FOR ALIGNMENT / TREE BUILDING */
    /* *********************************************************************************************** */
 
    /* Given an alignment in FASTA format, build a phylogenetic tree using the options indicated.
    */
    /* funcdef build_tree_from_fasta(fasta_alignment alignment, mapping<string,string>options) returns (newick_tree); */
    
    /* Given a set of sequences in FASTA format, construct a sequence alignment with the options indicated.
    */
    /* funcdef align_sequences(list<fasta> sequences, mapping<string,string>options) returns (fasta_alignment); */
 
 
    /* *********************************************************************************************** */
    /* METHODS FOR TREE VISUALIZATION */
    /* *********************************************************************************************** */

    /* Given a tree structure in newick, render it in HTML/JAVASCRIPT and return the page as a string. display_options
    provides a way to pass parameters to the tree rendering algorithm, but currently no options are recognized. */
    funcdef draw_html_tree(newick_tree tree, mapping<string,string>display_options) returns (html_file);
    

    funcdef contruct_tree(string genome_ref) returns (string tree);
};
