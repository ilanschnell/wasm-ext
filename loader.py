import os
import sys
from os.path import join, isfile
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location

from wasmtime import Module, Store, Instance

store = Store()

class _WasmtimeMetaFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if path is None or path == "":
            path = [os.getcwd()]  # top level import
            path.extend(sys.path)
        if "." in fullname:
            *parents, name = fullname.split(".")
        else:
            name = fullname
        for entry in path:
            py = join(str(entry), name + ".py")
            if isfile(py):
                continue
            wasm = join(str(entry), name + ".wasm")
            if isfile(wasm):
                return spec_from_file_location(fullname, wasm,
                                               loader=_WasmtimeLoader(wasm))
            wat = join(str(entry), name + ".wat")
            if isfile(wat):
                return spec_from_file_location(fullname, wat,
                                               loader=_WasmtimeLoader(wat))
        return None


class _WasmtimeLoader(Loader):
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        wasm_module = Module.from_file(store.engine, self.filename)

        instance = Instance(store, wasm_module, [])
        for export in wasm_module.exports:
            name = export.name
            func = instance.exports(store)[name]
            f = lambda *args: func(store, *args)
            print(name, id(f))
            module.__dict__[name] = f


sys.meta_path.insert(0, _WasmtimeMetaFinder())
