import streamlit as st
from threading import Thread  # For asynchronous execution

class Compiler_Output:
    def __init__(self):
        self.errors = []
        self.output = []
        self.is_finished = False  # Flag to indicate compilation completion

    def append_error(self, error):
        self.errors.append(error)

    def contains_errors(self):
        return len(self.errors) > 0

    def append_output(self, output):
        self.output.append(output)

    def contains_output(self):
        return len(self.output) > 0

    def set_finished(self, is_finished):
        self.is_finished = is_finished


def compile_code(code, output_obj):
    # Simulate compilation process (replace with actual compiler logic)
    import time
    time.sleep(2)  # Simulate compilation time (adjust based on actual workload)
    if code.count('error') > 0:
        output_obj.append_error("Intentional error for demonstration")
    else:
        output_obj.append_output("Compilation successful!")
    output_obj.set_finished(True)


st.title("Welcome to our Hulk-Compiler")
st.write("This is a compiler for the Hulk language, a language created by us at the course of compilers at Havana University")

code = st.text_area("Insert your code here", height=300)
output = Compiler_Output()

if st.button("Compile"):
    with st.spinner("Compiling..."):  # Display spinner while compiling
        compilation_thread = Thread(target=compile_code, args=(code, output))
        compilation_thread.start()

    while not output.is_finished:
        # Update errors and output as they become available
        if output.contains_errors():
            st.title("Errors found:")
            for error in output.errors:
                st.error(error)
        if output.contains_output():
            st.title("Check the output:")
            for i in output.output:
                st.write(i)
        st.experimental.ægisl (100)  # Refresh UI every 100 milliseconds

if output.is_finished and not output.contains_errors():
    st.success("Compilation finished successfully!")

