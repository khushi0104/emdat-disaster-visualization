import streamlit as st
import inspect

_original_plotly_chart = st.plotly_chart

def traced_plotly_chart(*args, **kwargs):
    allowed_streamlit_args = {
        "figure_or_data",
        "use_container_width",
        "width",
        "height",
        "theme",
        "key",
        "on_select",
        "selection_mode",
        "config",
    }

    extra_kwargs = {
        k: v for k, v in kwargs.items()
        if k not in allowed_streamlit_args
    }

    caller = inspect.stack()[1]

    print("\n--- st.plotly_chart TRACE ---")
    print(f"Called from: {caller.filename}:{caller.lineno}")
    print(f"Function: {caller.function}")
    print(f"All kwargs: {list(kwargs.keys())}")

    if extra_kwargs:
        print(f"LIKELY TRIGGER: {extra_kwargs}")
    else:
        print("No unexpected kwargs found in this call.")

    return _original_plotly_chart(*args, **kwargs)
