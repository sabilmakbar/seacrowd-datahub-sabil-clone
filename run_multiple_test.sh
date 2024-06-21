# example of use
# sh run_multiple_test.sh vlsp2020_mt_envi test_vlsp2020.log 1>test_vlsp2020.log 2>&1
# sh run_multiple_test.sh ud test_ud.log 1>test_ud.log 2>&1
# sh run_multiple_test.sh unisent test_unisent.log 1>test_unisent.log 2>&1

if [[ "$1" == "" ]]; then
    echo "Error: Missing the dataset name or output filepath"
    echo "./test_example.sh <dataset name> <output_filepath>"
    exit
fi

# python -m tests.test_seacrowd seacrowd/sea_datasets/$1/$1.py >> $2
# SUBSET_CONFIG=(aaz abx ace agn agt ahk akb alj alp amk aoz atb atd att ban bbc bcl bgr bgs bgz bhp bkd bku blw blz bpr bps bru btd bth bto bts btx bug bvz bzi cbk ceb cfm cgc clu cmo cnh cnw csy ctd czt dgc dtp due duo ebk fil gbi gor heg hil hnj hnn hvn iba ifa ifb ifk ifu ify ilo ind iry isd itv ium ivb ivv jav jra kac khm kix kje kmk kne kqe krj ksc ksw kxm lao lbk lew lex lhi lhu ljp lus mad mak mbb mbd mbf mbi mbs mbt mej mkn mnb mog mqj mqy mrw msb msk msm mta mtg mtj mvp mwq mwv mya nbe nfa nia nij nlc npy obo pag pam plw pmf pne ppk prf prk ptu pww sas sbl sda sgb smk sml sun sxn szb tbl tby tcz tdt tgl tha tih tlb twu urk vie war whk wrs xbr yli yva zom zyp pse mnx mmn lsi hlt gdg bnj acn)

# SUBSET_CONFIG=(EVBCorpus VLSP20-official basic indomain-news iwslt15 iwslt15-official ted-like wiki-alt)
SUBSET_CONFIG=(eng cmn)

for val in ${!SUBSET_CONFIG[@]}; do
    subset=${SUBSET_CONFIG[$val]}
    # schema=${SCHEMAS[$val]}
    echo "Executing Extractor on iteration no $((val+1)) of total ${#SUBSET_CONFIG[@]} for subset $subset"
    python -m tests.test_seacrowd seacrowd/sea_datasets/$1/$1.py --subset_id "$1_$subset" >> $2
    # echo "Executing Extractor on iteration no $((val+1)) of total ${#SUBSET_CONFIG[@]} for subset $subset and schema $schema"
    # python -m tests.test_seacrowd seacrowd/sea_datasets/$1/$1.py --subset_id "$1_$subset" --schema $schema >> $2
done

# SUBSET_CONFIG=(id_csui id_pud id_gsd vi_vtb tl_trg tl_ugnayan)
# schema="SEQ_LABEL"

# for val in ${!SUBSET_CONFIG[@]}; do
#     subset=${SUBSET_CONFIG[$val]}
#     echo "Executing Extractor on iteration no $((val+1)) of total ${#SUBSET_CONFIG[@]} for subset $subset and schema $schema"
#     python -m tests.test_seacrowd seacrowd/sea_datasets/$1/$1.py --subset_id "$1_$subset" --schema $schema >> $2
# done


# SUBSET_CONFIG=(id_csui id_gsd vi_vtb tl_trg)
# schema="KB"

# for val in ${!SUBSET_CONFIG[@]}; do
#     subset=${SUBSET_CONFIG[$val]}
#     echo "Executing Extractor on iteration no $((val+1)) of total ${#SUBSET_CONFIG[@]} for subset $subset and schema $schema"
#     python -m tests.test_seacrowd seacrowd/sea_datasets/$1/$1.py --subset_id "$1_$subset" --schema $schema >> $2
# done

# SUBSET_CONFIG=(id_csui id_pud tl_trg tl_ugnayan)
# schema="SEQ_LABEL"

# for val in ${!SUBSET_CONFIG[@]}; do
#     subset=${SUBSET_CONFIG[$val]}
#     echo "Executing Extractor on iteration no $((val+1)) of total ${#SUBSET_CONFIG[@]} for subset $subset and schema $schema"
#     python -m tests.test_seacrowd seacrowd/sea_datasets/$1/$1.py --subset_id "$1_$subset" --schema $schema >> $2
# done