# coding:utf-8
"""
create on Jan 24, 2022 By Wenyan YU

Function:

My first data web app using Streamlit

"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from datetime import time
from datetime import datetime
from PIL import Image
import time as sleeptime

st.title('Uber Pickups')

st.subheader("Layouts and Containers")
st.write("sidebar")
add_select_box = st.sidebar.selectbox(
    "Eyes of the Machine Senses Everything of Network.",
    ("MachineEyes", "ControlEyes(BGP)", "DataEyes(PING/TRACE)", "DNSEyes", "IXPEyes"))

st.write("You select %s Sidebar" % add_select_box)

if add_select_box == 'MachineEyes':

    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


    @st.cache
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data


    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = load_data(1000)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text('Loading data...done!(using st.cahce)')

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    st.subheader('Number of pickups by hour')
    hist_value = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
    st.bar_chart(hist_value)

    st.subheader('Map of all pickups')
    st.map(data)

    hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
    filter_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader(f'Map of all pickups at {hour_to_filter}:00')
    st.map(filter_data)

    st.write('Finish My first data Web APP Demo')
    st.subheader('- - - - - -  - Everything with Streamlit- - - - - - - - - -')
    st.markdown("### Markdown Demo")

    str_markdown = "##### GoCN 每日新闻（2022-01-04）\n" \
                   "1. [「GoCN 酷 Go 推荐」go 语言位操作库 — bitset](https://mp.weixin.qq.com/s/UcuKgKnt4fwrg3c-UHc3sw) \n" \
                   "2. [Go 通过 Map/Filter/ForEach 等流式 API 高效处理数据](https://mp.weixin.qq.com/s/7ATm_Zu7ib9MXf8ugy3RcA)\n" \
                   "3. [优化 Go 二进制文件的大小](https://prog.world/optimizing-the-size-of-the-go-binary)\n" \
                   "4. [通常是无符号](https://graphitemaster.github.io/aau)\n" \
                   "5. [将 Go 程序编译为 Nintendo Switch™ 的本机二进制文件](https://ebiten.org/blog/native_compiling_for_nintendo_switch.html)\n" \
                   "- 编辑: CDS\n" \
                   "- 订阅新闻: http://tinyletter.com/gocn\n" \
                   "- 招聘专区: https://gocn.vip/jobs\n" \
                   "- GoCN 归档: https://gocn.vip/topics/20927"

    st.markdown(str_markdown)

    st.caption('This is a string that explains something above.')
    code = '''def hello():
            print("Hello, Streamlit!")'''
    st.code(code, language='python')
    st.text("This is some text.\n")
    st.write(
        "Streamlit is an open-source Python library that makes it easy to create and share beautiful, \n"
        "custom web apps for machine learning and data science.\n"
        "In just a few minutes you can build and deploy powerful data apps. \n"
        "So let’s get started!")

    st.write("Using Latex")
    st.latex(r'''
         a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
         \sum_{k=0}^{n-1} ar^k =
         a \left(\frac{1-r^{n}}{1-r}\right)
         ''')

    st.subheader("Data Display")
    st.write("Using DataFrame")
    df = pd.DataFrame(
        np.random.randn(50, 20),
        columns=['col %d' % i for i in range(20)])
    st.dataframe(df.style.highlight_max(axis=0, color='green'))  # same as st.write(df)

    st.write("Using Table(The table in this Case is static)")
    df = pd.DataFrame(
        np.random.randn(10, 5),
        columns=['col %d' % i for i in range(5)])
    st.table(df.style.highlight_max(axis=0, color='green'))

    st.write("Using Metric")
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    st.write("Using Json")
    st.json({
         'foo': 'bar',
         'baz': 'boz',
         'stuff': [
             'stuff 1',
             'stuff 2',
             'stuff 3',
             'stuff 5',
         ],
     })
    st.subheader("Chart")
    st.write("Using Line Chart")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
    st.line_chart(chart_data)

    st.write("Using Area Chart")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
    st.area_chart(chart_data)

    st.write("Using Bar Chart")
    chart_data = pd.DataFrame(
        np.random.randn(50, 3),
        columns=['a', 'b', 'c'])
    st.bar_chart(chart_data)

    st.write("Using Map")
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])
    st.map(df)

    st.write("Using 3rd Pylot(no arguments in st.pylot(), which is not thread-safe)")
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)
    st.pyplot(fig)

    # st.write("Using 3rd Plotly(Display an interactive Plotly chart)")
    #
    # # Add histogram data
    # x1 = np.random.randn(200) - 2
    # x2 = np.random.randn(200)
    # x3 = np.random.randn(200) + 2
    #
    # # Group data together
    # hist_data = [x1, x2, x3]
    #
    # group_labels = ['Group 1', 'Group 2', 'Group 3']
    #
    # fig = ff.create_distplot(
    #          hist_data, group_labels, bin_size=[.1, .25, .5])
    #
    # # Plot!
    # st.plotly_chart(fig, use_container_width=True)

    st.write("The third party Chart also include Altair, Vega_lite, Plotly, Bokeh, Pydeck, Graphviz.")

    st.subheader("Input Widgets")
    st.write("Using Button")
    if st.button('Say Hello'):
        st.write('Why hello there')
    else:
        st.write('Goodbye')

    st.write("Using Download Button")


    @st.cache
    def convert_df(inner_df):
        return inner_df.to_csv().encode('utf-8')


    my_large_df = pd.DataFrame(
        np.random.randn(50, 20),
        columns=['col %d' % i for i in range(20)])
    csv = convert_df(my_large_df)

    st.download_button(
        label='Download data as CSV',
        data=csv,
        file_name='large_df.csv',
        mime='text/csv')

    st.write("Using Checkbox")
    agree = st.checkbox('I agree')
    if agree:
        st.write('Great!')

    st.write('Using Radio')
    genre = st.radio(
        "What's your favorite movie genre",
        ('Comedy', 'Drama', 'Documentary'))
    if genre == 'Comedy':
        st.write('You select comedy.')
    else:
        st.write("You didn't select comedy.")

    st.write("Using Selectbox")
    option = st.selectbox(
        'How would you like to be contacted?',
        ('Email', 'Home Phone', 'Mobile Phone'))
    st.write('You selected:', option)

    st.write("Using Multiselect")
    options = st.multiselect(
        'What are your favorite colors',
        ['Green', 'Yellow', 'Red', 'Blue'],
        ['Yellow', 'Red'])
    st.write('You selected:', options)

    st.write("Using Slider")
    age = st.slider('How old are you?', 0, 130, 25)
    st.write("I'm ", age, 'years old.')

    st.write("Using Slider(here's an example of a range slider)")
    values = st.slider(
        'select a range of values',
        0.0, 100.0, (25.0, 75.0))
    st.write('Values:', values)

    st.write("Using Slider(This is a range time slider)")
    appointment = st.slider(
        'Schedule your appointment:',
        value=(time(11, 30), time(12, 45)))
    st.write("You're scheduled for:", appointment)

    st.write("Using Slider(This is a datetime slider)")
    start_time = st.slider(
        "When do you start?",
        value=datetime(2020, 1, 1, 9, 30),
        format="MM/DD/YY - hh:mm")
    st.write("Start time:", start_time)

    st.write("Using Select Slider")
    color = st.select_slider(
         'Select a color of the rainbow',
         options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'])
    st.write('My favorite color is', color)

    st.write("Using Select Slider(a range of select slider)")
    start_color, end_color = st.select_slider(
         'Select a range of color wavelength',
         options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'],
         value=('red', 'blue'))
    st.write('You selected wavelengths between', start_color, 'and', end_color)

    st.write("Using Text Input")
    title = st.text_input('Movie title', 'Life of Brain :smile:')
    st.write('The current movie title is', title)

    st.write("Using Number Input")
    number = st.number_input('Insert a number')
    st.write('The current number is', number)

    st.write("Using Text Area Input")
    txt = st.text_area('Text to analyze', '''
         It was the best of times, it was the worst of times, it was
         the age of wisdom, it was the age of foolishness, it was
         the epoch of belief, it was the epoch of incredulity, it
         was the season of Light, it was the season of Darkness, it
         was the spring of hope, it was the winter of despair, (...)
         :tada: :tada: :tada:
         ''')
    st.write('Area Text:', txt)

    st.write("Using Date Input")
    d = st.date_input(
        "When's your birthday",
        datetime(2019, 7, 6))
    st.write('Your birthday is:', d)

    st.write("Using Time Input")
    t = st.time_input("Set an alarm for", time(8, 45))
    st.write('Alarm is set for', t)

    st.write("Using File Uploader")
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)

    st.write("Using Camera Input")
    picture = st.camera_input("Take a picture")
    if picture:
        st.image(picture)


    st.subheader("Media")
    with st.expander("See Detail"):
        st.write("image")
        image = Image.open("D:/Code/Crawler4Caida/076Streamlit/sunrise.png")
        st.image(image, caption='Sunrise by the mountains')

        st.subheader("audio")
        audio_file = open('D:/Code/Crawler4Caida/076Streamlit/The Sounds Of Silence.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')

        st.write("video")
        video_file = open("D:/Code/Crawler4Caida/076Streamlit/star.mp4", "rb")
        video_bytes = video_file.read()
        st.video(video_bytes)






    st.write("columns")

    with st.expander("See Detail"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("A cat")
            st.image("https://static.streamlit.io/examples/cat.jpg")

        with col2:
            st.header("A dog")
            st.image("https://static.streamlit.io/examples/dog.jpg")

        with col3:
            st.header("An owl")
            st.image("https://static.streamlit.io/examples/owl.jpg")

    st.write("columns(call methods directly in the returned objects)")
    with st.expander("See Detail"):
        col1, col2 = st.columns([3, 1])  # [3, 1] is the ratio of width
        data = np.random.randn(10, 1)

        col1.subheader("A wide column with a chart")
        col1.line_chart(data)

        col2.subheader("A narrow column with the data")
        col2.write(data)

    st.write("expander")
    st.line_chart({"data": [1, 5, 2, 6, 2, 1]})
    with st.expander("See explanation"):
        st.write("""
                The chart above shows some numbers I picked for you.
                I rolled actual dice for these, so they're *guaranteed* to 
                be random.
        """)
        st.image("https://static.streamlit.io/examples/dice.jpg")

    st.write("container")
    container = st.container()
    with container:
        st.write("This is inside the container")
        # You can call any Streamlit command, including custom components:
        st.bar_chart(np.random.randn(50, 3))
    st.write("This is outside the container")
    container.write("This in insider too(out of order!)")

    st.write("empty(Overwriting elements in-place using 'with' notation)")
    with st.empty():
        for seconds in range(2):
            st.write(f"{seconds} seconds have passed")
            sleeptime.sleep(1)
        st.write("2 second over!")

    st.write("empty(Replacing several elements, then clearing them)")
    placeholder = st.empty()  # only single element can be exist

    # Replace the placeholder with some text:
    placeholder.text("Hello")

    # Replace the text with a chart:
    placeholder.line_chart({"data": [1, 5, 2, 6]})

    # Replace the chart with several elements:
    with placeholder.container():
        st.write("This is one element")
        st.write("This is another")

    # Clear all those elements:
    placeholder.empty()
elif add_select_box == 'ControlEyes(BGP)':
    st.subheader("Status Elements")
    st.write("progress")

