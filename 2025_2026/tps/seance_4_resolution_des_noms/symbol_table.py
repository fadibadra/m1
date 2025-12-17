import symtable

def _describe_symbol(sym):
    assert type(sym) == symtable.Symbol
    print("Symbol:", sym.get_name(),end=' ')

    for prop in [
            'referenced', 'imported', 'parameter',
            'global', 'declared_global', 'local',
            'free', 'assigned', 'namespace']:
        if getattr(sym, 'is_' + prop)():
            print(prop,' ',end='')
    print()

def _describe_symtable(st, recursive=True, indent=0):
    def print_d(s, *args):
        prefix = ' ' * indent
        print(prefix + s, *args)

    assert isinstance(st, symtable.SymbolTable)
    print_d('Symtable: type=%s, id=%s, name=%s' % (
                st.get_type(), st.get_id(), st.get_name()))
    print_d('  nested:', st.is_nested())
    print_d('  has children:', st.has_children())
    print_d('  identifiers:', list(st.get_identifiers()))
    for sym in st.get_symbols():
        assert type(sym) == symtable.Symbol
        sym_props = '  '+ sym.get_name() + ' is '
        for prop in [
                'referenced', 'imported', 'parameter',
                'global', 'declared_global', 'local',
                'free', 'assigned', 'namespace']:
            if getattr(sym, 'is_' + prop)():
                sym_props = sym_props + prop + ' '
        print_d(sym_props)
    
    if recursive:
        for child_st in st.get_children():
            _describe_symtable(child_st, recursive, indent + 5)

def describe_symbol_table(code):
    _describe_symtable(symtable.symtable(code,'example_code.py','exec'))



