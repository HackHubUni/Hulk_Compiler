import streamlit as st
class Compiler_Output:
    def __init__(self):
        self.errors = []
        self.output = []

    def append_error(self, error):
        self.errors.append(error)

    def contains_errors(self):
        return len(self.errors) > 0
    
    def append_output(self, output):
        self.output.append(output)
    
    def contains_output(self):
        return len(self.output) > 0

st.title("Welcome to our Hulk-Compiler")
st.write("This is a compiler for the Hulk language, a language created by us at the course of compilers at Havana University")
code = st.text_area("Insert your code here", height=300)
output = Compiler_Output()
if st.button("Compile"):
    st.write("Compiling...")
    #mandar a ejecitar el proyecto code es el string con el codigo y la instancia de los errorres
    # devolver el codigo en un string code 
   

    if output.contains_errors():
        st.title("Errors found:")
        for error in output.errors:
            st.write(error)
    else : 
        
        st.write("Compilation finished")
        st.title("Check the output:")
        if output.contains_output():
            for i in output.output:
                st.write(i)
        else:
            st.write("No output found, action finished successfully")


    
