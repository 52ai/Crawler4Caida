import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
st.set_page_config(page_icon="🌴", page_title="Tabulator表格", layout="wide")

file = st.file_uploader("请上传文件", type=["csv"])

if file is not None:
    df = pd.read_csv(file, encoding="gbk")

    def draw_table(df, height, width):
        columns = df.columns
        column_selection = []
        column_selection.append("""<select id="filter-field" style="font-size:15px;background:white;color:black;border-radius:15%;border-color:grey;">""")
        for i in range(len(columns)):
            column_selection.append("""<option value='"""+str(columns[i])+"""'>"""+str(columns[i])+"""</option>""")
        column_selection.append("""</select>""")
        table_data = df.to_dict(orient="records")
        column_setting = []
        column_setting.append("""{rowHandle:true, formatter:"handle", headerSort:false, frozen:true, width:30, minWidth:30}""")
        for y in range(df.shape[1]):
            column_setting.append({"title":columns[y], "field":columns[y], "width": 200,"sorter":"string", "hozAlign":"center", "headerFilter":"input","editor": "input"})

        components.html("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tabulator Example</title>
            <link href="https://unpkg.com/tabulator-tables@4.8.1/dist/css/tabulator_modern.min.css" rel="stylesheet">
            <script type="text/javascript" src="https://unpkg.com/tabulator-tables@4.8.1/dist/js/tabulator.min.js"></script>
            <script type="text/javascript" src="https://moment.github.io/luxon/global/luxon.min.js"></script>
            <script type="text/javascript" src="https://oss.sheetjs.com/sheetjs/xlsx.full.min.js"></script>
        </head><body>
            <div style="margin-left:30%;">"""+"".join(column_selection)+
            """<select id="filter-type" style="font-size:15px;background:#00ccff;color:white;border-radius:15%;border-color:white;">
                <option value="like">like</option>
                <option value="=">=</option>
                <option value="<"><</option>
                <option value="<="><=</option>
                <option value=">">></option>
                <option value=">=">>=</option>
                <option value="!=">!=</option>
              </select>
              <input id="filter-value" type="text" placeholder="填写要筛选的内容" style="font-size:15px;border-color:grey;border-radius:5%">
              <button id="filter-clear" style="font-size:15px;background:#00ccff;color:white;border-radius:15%;border-color:white;">清除筛选</button>
              <button id="download-csv" style="font-size:15px;background:#00ccff;color:white;border-radius:15%;border-color:white;">下载CSV</button>
              <button id="download-xlsx" style="font-size:15px;background:#00ccff;color:white;border-radius:15%;border-color:white;">下载XLSX</button>
              <button id="download-html" style="font-size:15px;background:#00ccff;color:white;border-radius:15%;border-color:white;">下载HTML</button>
            </div><script type="text/javascript">
                var fieldEl = document.getElementById("filter-field");
                var typeEl = document.getElementById("filter-type");
                var valueEl = document.getElementById("filter-value");
                function customFilter(data){
                    return data.car && data.rating < 3;
                }function updateFilter(){
                  var filterVal = fieldEl.options[fieldEl.selectedIndex].value;
                  var typeVal = typeEl.options[typeEl.selectedIndex].value;
                  var filter = filterVal == "function" ? customFilter : filterVal;
                  if(filterVal == "function" ){
                    typeEl.disabled = true;
                    valueEl.disabled = true;
                  }else{
                    typeEl.disabled = false;
                    valueEl.disabled = false;
                  }
                  if(filterVal){
                    table.setFilter(filter,typeVal, valueEl.value);
                  }
                }
                document.getElementById("filter-field").addEventListener("change", updateFilter);
                document.getElementById("filter-type").addEventListener("change", updateFilter);
                document.getElementById("filter-value").addEventListener("keyup", updateFilter);
                document.getElementById("filter-clear").addEventListener("click", function(){
                  fieldEl.value = "";
                  typeEl.value = "=";
                  valueEl.value = "";
                  table.clearFilter();
                });
            </script>
            <script type="text/javascript">
                var table = new Tabulator("#example-table", {
                    ajaxURL:"http://www.getmydata.com/now",
                });
                document.getElementById("download-csv").addEventListener("click", function(){
                    table.download("csv", "data.csv");
                });
                document.getElementById("download-xlsx").addEventListener("click", function(){
                    table.download("xlsx", "data.xlsx", {sheetName:"My Data"});
                });
                document.getElementById("download-html").addEventListener("click", function(){
                    table.download("html", "data.html", {style:true});
                });
            </script><div id="players" style="margin-left:16%;"></div>"""+
            """<script type="text/javascript">
                var tabledata = ["""+','.join(list(map(str,table_data)))+"""];"""+
            """var table = new Tabulator("#players", {
                    height: 320,
                    data: tabledata,
                    layout: "fitDataTable",
                    movableRows:true,
                    resizableColumnFit:true,
                    pagination: "local",
                    paginationSize: 5,
                    tooltips: true,
                    columns: ["""+','.join(list(map(str,column_setting)))+"""],});</script></body></html>""", height=height, width=width)
    draw_table(df, 500, 1200)
