import os
import pickle

from easy_dc.defs import *


def pickleload(filename, mode='rb', show=False, raise_error=False) -> Any:
    """
    Load object from a .pickle file
    """
    filename = f'{filename}.pickle' if 'pickle' not in filename else filename
    try:
        with open(filename, mode) as f:
            if show:
                print(f'🗃️ {filename}')
            try:
                return pickle.load(f)
            except pickle.UnpicklingError:
                print(filename)
    except EOFError:
        print(f"💩 {filename}")
        if raise_error:
            raise FileNotFoundError


def picklesave(to_pickle, filename, show=True, space=True) -> str:
    """
    Serialize object to .pickle file
    """
    if "pickle" not in filename:
        filename += ".pickle"
    with open(filename, 'wb') as outfile:
        pickle.dump(to_pickle, outfile, protocol=pickle.HIGHEST_PROTOCOL)
    if show:
        print(f' 💾 {filename}')
    return f'💾{" " if space else ""}{filename}'


def get_G(ORD, make=False) -> Graph:
    """
    Get DC graph.
    """
    from easy_dc.make import make_dcgraph
    if make:
        return make_dcgraph(ORD, save=True)
    try:
        if (loaded := pickleload(os.path.join(FP_GRAPHS, str(ORD)), )) is None:
            return make_dcgraph(ORD, save=True)
        return loaded
    except FileNotFoundError:
        print('GRAPH NOT IN FILE, MAKING....')
        save_G(make_dcgraph(ORD))
        return get_G(ORD)


def save_G(G):
    """
    Get DC graph.
    """
    picklesave(G, os.path.join(FP_GRAPHS, str(len(G['A']))))
