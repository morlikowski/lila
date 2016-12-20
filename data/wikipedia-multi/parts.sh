#!/bin/sh
MULTI_TR="-t wikipedia-multi/docsUR1 -t wikipedia-multi/docsUR2 -t wikipedia-multi/docsUR3 -t wikipedia-multi/docsUR4 -t wikipedia-multi/docsUR5"
MULTI_TE="-e wikipedia-multi/docsUE1 -e wikipedia-multi/docsUE2 -e wikipedia-multi/docsUE3 -e wikipedia-multi/docsUE4 -e wikipedia-multi/docsUE5"
python partition.py -o partitions/mono-mono   -t wikipedia-multi/docsMR -e wikipedia-multi/docsME
python partition.py -o partitions/mono-multi  -t wikipedia-multi/docsMR ${MULTI_TE}
python partition.py -o partitions/multi-mono  ${MULTI_TR} -e wikipedia-multi/docsME
python partition.py -o partitions/multi-multi ${MULTI_TR} ${MULTI_TE} 
