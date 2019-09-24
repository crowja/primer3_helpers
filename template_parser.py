def _find_regions(seq, delim_open, delim_close):

    """Locate the regions marked by a delimiter pair.

    starts, widths = _find_regions(seq_template, "[", "]")

    seq:         Primer3 sequence template. E.g., ACGT[TAC]GCC[CCGA]ATT.
    delim_open:  Symbol signifying next base in the sequence template begins a region.
    delim_close: Symbol signifying previous base in the sequence template ends a region.
    """

    pstate_null = 0  # default
    pstate_open = 1  # found an open delimiter

    s = seq.replace(" ", "")  # remove whitespace from input sequence

    pos = 0
    start = -1
    width = 0
    state = pstate_null
    starts = []
    widths = []

    for idx in range(len(seq)):
        if s[idx] in "acgtnxACGTNX":  # found a base
            if state == pstate_null:
                pass
            elif state == pstate_open:
                if width > 0:  # already found the region start, extend the width
                    width += 1
                else:  # we haven't located the region start yet so this is it
                    start = pos
                    width = 1
            else:
                exit(1)  # TODO this can't happen
            pos += 1
        elif s[idx] == delim_open:  # an opening delimiter
            if state == pstate_null:
                # print("FOUND OPEN AT ", pos)
                state = pstate_open
            elif state == pstate_open:
                raise ValueError(
                    f"Sequence string parse error: unexpected opening delimiter {delim_open} found."
                )
                pass
            else:
                pass  # TODO this can't happen!
        elif s[idx] == delim_close:  # a closing delimiter
            if state == pstate_null:
                raise ValueError(
                    f"Sequence string parse error: unexpected closing delimiter {delim_close} found."
                )
            elif state == pstate_open:
                print(f"Region is {start}, {width}")
                width = 0
                state = pstate_null
            else:
                pass  # TODO this can't happen, throw an exception
        else:  # A character to ignore, e.g. a different delimiter
            pass


seq = "GAG{[GT]AG[TCAGTAGACN]ATGACN-ACT-GACGATGCAGACNACACACACACACACAGCACACAGGTATTAGTGGGCCATTCG[ATCC][CGACCCAAAT]CGATAGCTACGAT-G}ACG"

# For [] regions: 4, 2; 8, 10; 81, 4
_find_regions(seq, "[", "]")
