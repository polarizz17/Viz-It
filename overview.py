import base64
import pandas as pd
import os
import streamlit as st
import matplotlib.pyplot as plt

class Overview():
    def __init__(self, title, background, font):
        bg_ext = background.split('.')[-1]
        self.font = font
        st.markdown(
            f"""<style>
                .reportview-container {{
                    background: url(data:image/{bg_ext};base64,{base64.b64encode(open(background, "rb").read()).decode()})
                    }}
                    background-position: center;
                    background-repeat: no-repeat;
                    background-size: cover;
                    }}
                </style>""",
            unsafe_allow_html=True
        )
        st.markdown(f"<h1 style='text-align: center; color:#{font};'>{title}</h1>",
                    unsafe_allow_html=True)
        super(Overview, self).__init__()

    def data_handler(self):
        self.file = st.file_uploader("Upload data", type=['csv'])
        _,_,_,col,_,_,_ = st.columns(7)
        with col:
            self.delete = st.button('DELETE DATA')
        if self.file is not None:
            try:
                with open('data.csv', "wb") as f:
                    f.write(self.file.getbuffer())
            except:
                st.write('Invalid format...')
        if self.delete and os.path.isfile('data.csv'):
            os.remove('data.csv')
            st.file = None
    def fetch_data(self):
        self.data = pd.DataFrame({})
        if os.path.isfile('data.csv'):
            self.data = pd.read_csv('data.csv')
    def column_overview(self):
        if len(self.data.columns) > 0:
            st.markdown(f"<h3 style='text-align: center; color:#{self.font};'>Column Overview</h3>",
                        unsafe_allow_html=True)
            fig, ax = plt.subplots(1,2,figsize = (15,5))
            ax[0].pie(self.data.dtypes.value_counts().values, labels = self.data.dtypes.value_counts().index)
            ax[0].set_title('Pie-Chart')
            ax[1].bar(x = self.data.dtypes.value_counts(), height = self.data.dtypes.value_counts().values, tick_label = self.data.dtypes.value_counts().index)
            ax[1].set_title('Bar diagram')
            fig.suptitle('Column Overview')
            st.pyplot(fig = fig)

    def null_overview(self):
        if len(self.data.columns) > 0:
            st.markdown(f"<h3 style='text-align: center; color:#{self.font};'>Missing Value Analysis</h3>",
                        unsafe_allow_html=True)
            fig = plt.figure(figsize=(15, 5))
            plt.bar(self.data.isnull().sum().index,self.data.isnull().sum().values)
            plt.xticks(rotation = 90)
            plt.yticks([])
            st.pyplot(fig = fig)

    def fire(self):
        self.data_handler()
        self.fetch_data()
        self.column_overview()
        self.null_overview()


if __name__ == '__main__':
    app = Overview('Viz-it','src/bg.png','#9ffff')
    app.fire()






