import re

def _find_regions(seq, delim_open, delim_close):

    """Locate the regions marked by a delimiter pair.

    starts, widths = _find_regions(seq_template, "[", "]")

    seq:         Primer3 sequence template. E.g., ACGT[TAC]GCC[CCGA]ATT.
    delim_open:  Symbol signifying next base in the sequence template begins a region.
    delim_close: Symbol signifying previous base in the sequence template ends a region.
    """

    # Parser states
    pstate_null = 0  # default
    pstate_open = 1  # found an open delimiter

    s = seq.replace(" ", "")  # remove whitespace from input sequence

    pos = 0  # track where we are in the sequence of bases only
    start = -1  # beginning of current region
    width = 0  # (current) width of current region
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
                starts.extend([start + 1])  # convert to base 1 indexing
                widths.extend([width])
                width = 0
                state = pstate_null
            else:
                pass  # TODO this can't happen, throw an exception
        else:  # A character to ignore, e.g. a different delimiter
            pass

    return starts, widths


def _find_junctions(seq):

    """Locate the junctions marked by a delimiter "-".

    locs = _find_junctions(seq_template)

    seq:         Primer3 sequence template. E.g., ACGT[TAC]G-CC[CCGA]ATT.
    """

    re1 = re.compile("[<>{}\[\] ]+")
    re2 = re.compile("[\-]+")
    t = re1.sub("", seq) # first remove region delimiters, whitespace, ...
    s = re2.sub("-", t) # ... then squash adjacent repeated "-" symbols
    print("NEW SEQ ", s)


if __name__ == "__main__":

    # For [] regions: 4, 2; 8, 10; 81, 4; 85, 10
    seq = "GAG{[GT]AG[TCAGTAGACN]ATGACN-ACT-GACGATGCAGACNACACACACACACACAGCACACAGGTATTAGTGGGCCATTCG[ATCC][CGACCCAAAT]CGATAGCTACGAT-G}ACG"

    starts, widths = _find_regions(seq, "[", "]")
    print("STARTS: ", starts)
    print("WIDTHS: ", widths)

    # For [] regions: 4, 4; 8, 5
    seq = "AAA[AAAA][AAAAA]AAA"
    starts, widths = _find_regions(seq, "[", "]")
    print("STARTS: ", starts)
    print("WIDTHS: ", widths)

    # For [] regions: 1, 14
    seq = "[AAAAAAAAAAAAAA]"
    starts, widths = _find_regions(seq, "[", "]")
    print("STARTS: ", starts)
    print("WIDTHS: ", widths)

    # For [] regions: 1, 1; 2, 1; 3, 1; 4, 1; 5, 10
    seq = "[A][A][A][A][AAAAAAAAAA]"
    starts, widths = _find_regions(seq, "[", "]")
    print("STARTS: ", starts)
    print("WIDTHS: ", widths)
   
    seq = "aaa-aaaa-aaaaa-aaaa---a--a-a"
    _find_junctions(seq)
