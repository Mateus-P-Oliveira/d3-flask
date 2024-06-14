import glob
import os
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import plotly.graph_objects as go
import plotly.express as px #Trocar px e go por funções do matplotlib
#import mpld3
import base64
from io import BytesIO



import plotly.io as pio

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
#from mpl_toolkits.mplot3d import Axes3D


pio.renderers.default='browser'

class MyPlots:

    def __init__(self): #Inicializa a classe
        self.list_of_files = None
        self.options = None
        self.files_data_complete = None
        self.files_data = None
        self.line = None
        self.file1 = None
        self.file2 = None
        self.contours = dict(start = None, end = None, size = None, showlines= True)
        self.data = pd.DataFrame(columns=["x","y","recente","antigo","diff"])
        self.data1 = None
        self.data2 = None
        self.scale_steps = 20
        self.complete_df = None

    def set_data1(self, file): #Carrega os dados
        self.file1 = file
        self.date1 = self.files_data[self.files_data['file'].str.contains(file)]['data'].iloc[0]
        self.data1 = self.load_grid(self.path + file)
        datatemp = self.load_data(self.path + file)
        datatemp = datatemp.drop(columns = ["x1","x2","x3","x4","x5","x6","x7","x8","x9"])
        datatemp = datatemp.rename(columns = {"res": "recente"})
        self.data = self.data.drop(columns= ["recente"])
        self.data = self.data.merge(datatemp, on = ["x", "y"], how = "outer")
        self.data["diff"] = 100*(self.data["recente"]/self.data["antigo"]-1)
        print(self.data)
        self.set_scale()

    def set_data2(self, file):#Carrega os dados 
        self.file2 = file
        self.date2 = self.files_data[self.files_data['file'].str.contains(file)]['data'].iloc[0]
        self.data2 = self.load_grid(self.path + file)
        datatemp = self.load_data(self.path + file)
        datatemp = datatemp.drop(columns = ["x1","x2","x3","x4","x5","x6","x7","x8","x9"])
        datatemp = datatemp.rename(columns = {"res": "antigo"})
        self.data = self.data.drop(columns= ["antigo"])
        self.data = self.data.merge(datatemp, on = ["x", "y"], how = "outer")
        self.data["diff"] = 100*(self.data["recente"]/self.data["antigo"]-1)
        print(self.data)
        self.set_scale()

    def clean_data(self): #Limpa 
        self.file1 = None
        self.data1 = None
        self.file2 = None
        self.data2 = None

    def load_files(self, path): #Carrega dados
        self.path = path
        files = glob.glob(self.path + "*.dat")
        files = [os.path.join(os.path.dirname(file), os.path.basename(file)).replace('\\', '/') for file in files]
        self.files_data_complete = pd.DataFrame(files, columns=['file'])
        self.files_data_complete['data'] = [x.split('/')[-1][:8] for x in self.files_data_complete['file']]
        self.files_data_complete.sort_values(by='data', ascending=False, inplace=True)
        self.files_data_complete['data'] = [self.reorder_date(x) for x in self.files_data_complete['data']]
        self.list_of_files = files
        return self.files_data_complete['file'].to_list()

    def reorder_date(self, date_str): #Organiza as informações
        date = [date_str[2:4],date_str[4:6],date_str[6:]]
        return f'{date[2]}_{date[1]}_{date[0]}'

    def to_grid(self, points, Z): #Aqui faz o grafico, manter essa aqui
        X1 = sorted(np.unique(points[0]))
        Y1 = sorted(np.unique(points[1]))
        grid_x, grid_y = np.meshgrid(X1,Y1)
        gridd = griddata(points, Z, (grid_x,grid_y), method='linear')
        return X1, Y1, grid_x, grid_y, gridd

    def load_data(self, file): #Carrega os valores para os graficos
        data = pd.read_csv(file, sep=';')
        data = data.dropna()
        data.columns = ['x1','x2','x3','x4','x5','x6','x7','x8','x9', 'res']
        data.x2 = round(data.x2, 1)
        data.x4 = round(data.x4, 1)
        data.x6 = round(data.x6, 1)
        data.x8 = round(data.x8, 1)
        ab = abs(data.x2 - data.x4).max()
        mn = abs(data.x6 - data.x8).max()
        if ab > mn:
            data['x'] = (data.x2 + data.x4)/2
            data['y'] = -0.2*abs(data.x2 - data.x4)
        else:
            data['x'] = (data.x6 + data.x8)/2
            data['y'] = -0.2*abs(data.x6 - data.x8)
        return data

    def load_grid(self, file): #Faz a grade do grafico
        data = self.load_data(file)
        X, Y, grid_x, grid_y, data = self.to_grid((data.x,data.y), data.res)
        self.X = X
        self.Y = Y
        self.grid_x = grid_x
        self.grid_y = grid_y
        data[data == 0] = np.nan
        return data




    def return_contour(self, data, cont=None, log=False, title=''):
        if log:
            data = np.log(data)

        X, Y = np.meshgrid(self.X, self.Y)
        
        levs = np.linspace(np.log10(np.nanmin(data)), np.log10(np.nanmax(data)), 20)
        levs = np.power(10, levs)
        
        fig, ax = plt.subplots()
        plt.tight_layout()

        contour = ax.contourf(X, Y, data, levels=levs, cmap='RdBu')
        plt.colorbar(contour)
        ax.set_title(title.replace('.dat', ''))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.show()
        
        # Cria um dicionário com os dados do gráfico
        graph_data = {
            'title': title.replace('.dat', ''),
            'xlabel': 'X',
            'ylabel': 'Y',
            'data': data.tolist(),  # Converte os dados para lista
            'X': X.tolist(),  # Converte as coordenadas X para lista
            'Y': Y.tolist(),  # Converte as coordenadas Y para lista
            'levels': levs.tolist(),  # Converte os níveis para lista
            'cmap': 'RdBu'
        }
        
        # Fecha a figura para liberar memória
        plt.close(fig)
        
        # Retorna o dicionário com os dados do gráfico
        return graph_data



    
    def return_contour_generic(self, data, X, Y, cont = None, log = False, title = ''): #Acho que vou mudar isso aqui #Mudar para MatplotLib
        if log:
            data = np.log(data)

        levs = np.linspace(np.log10(np.nanmin(data)), np.log10(np.nanmax(data)),20)
        levs = np.power(10, levs)

        fig, ax = plt.subplots()
        ax.figure()
        contour = ax.contourf(X, Y, data, levels=levs, cmap='RdBu')
        plt.colorbar(contour)
        ax.set_title(title.replace('.dat', ''))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.show()

        return fig

    def slice_avg(self):
        df = pd.DataFrame()
        df['dia'] = self.options[self.options.index(self.file1):self.options.index(self.file2) + 1][::-1]
        df['data'] = [self.reorder_date(x[:8]) for x in df['dia']]
        df['avg'] = [np.nanmean(self.load_grid(self.path + x)) for x in df['dia']]
        df['acumulado'] = 100 * (df['avg'] / df['avg'].iloc[0] - 1)
        df['movel'] = 0
        for x in range(1, len(df['avg'])):
            df.loc[x, 'movel'] = 100 * (df['avg'][x] / df['avg'][x - 1] - 1)

        # Criação do gráfico de linha usando matplotlib
        fig, ax = plt.subplots()
        ax.plot(df['data'], df['acumulado'], label='Acumulado', marker='o')
        ax.plot(df['data'], df['movel'], label='Móvel', marker='o')
        ax.set_title('Evolução')
        ax.set_xlabel('Data')
        ax.set_ylabel('Percentual')
        ax.legend()
        ax.grid(True)
        fig.update_layout()

        return fig

    def set_scale(self): #Ajusta a escala
        d1_max = np.nan
        d1_min = np.nan
        d2_max = np.nan
        d2_min = np.nan
        if self.data1 is not None:
            d1_max = np.nanmax(np.log(self.data1))
            d1_min = np.nanmin(np.log(self.data1))
        if self.data2 is not None:
            d2_max = np.nanmax(np.log(self.data2))
            d2_min = np.nanmin(np.log(self.data2))
        Max = np.nanmax([d1_max, d2_max])
        Min = np.nanmin([d1_min, d2_min])
        self.contours['start'] = Min
        self.contours['end'] = Max
        self.contours['size'] = (Max-Min)/self.scale_steps

    def complete_list(self): # Completa os valores da lista
        files = self.options[self.options.index(self.file1):self.options.index(self.file2)+1]
        df = pd.DataFrame()
        count = 0
        # for file in files:
        #     data = self.load_data(self.path + file)
        #     data['z'] = count
        #     df = pd.concat([df,data[['res', 'x', 'y', 'z']]])
        #     count += 1
        for file in files:
            df_temp = pd.DataFrame()
            data = self.load_grid(self.path + file)
            df_temp['res'] = data.flatten()
            df_temp['x'] = self.grid_x.flatten()
            df_temp['y'] = self.grid_y.flatten()
            df_temp['z'] = count
            df = pd.concat([df,df_temp])
            count += 1
        self.complete_df = df
        return df

    import matplotlib.pyplot as plt

    def return_slice(self, layer, norm=False, cont=None, color='RdBu'):
        df = self.complete_df[self.complete_df['y'] == self.Y[layer]]
        df = df.dropna()
        X, Y, grid_x, grid_y, data = self.to_grid((df.x, df.z), df.res)
        if norm:
            print(0)
    
        # Criação do gráfico de contorno usando matplotlib
        fig, ax = plt.subplots()
        CS = ax.contourf(X, Y, data, levels=cont, colors=color)
        plt.colorbar(CS)
        ax.set_title(f'Profundidade {self.Y[layer]} metros.')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
    
        # Retorno da figura e dos valores mínimo e máximo de data
        return fig, np.nanmin(data), np.nanmax(data)



    def return_volume(self, data, opacity=0.5):
        # Transforma os valores de res para o logaritmo
        data['res'] = np.log(data['res'])
    
        # Cria uma figura e um eixo 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    
        # Plota o volume
        ax.scatter(data['z'], data['x'], data['y'], c=data['res'], cmap='jet', alpha=opacity)
    
        # Configuração do título e dos rótulos dos eixos
        ax.set_title('Volume')
        ax.set_xlabel('Dias')
        ax.set_ylabel('Distância')
        ax.set_zlabel('Profundidade')
    
        # Ajusta as margens
        ax.margins(0.05)
    
        # Retorna a figura
        return fig



if __name__ == '__main__':
    myplots = MyPlots()
    myplots.load_files("files")
    print(myplots.list_of_files)
    # myplots.options = [x.replace('files\\', '') for x in myplots.list_of_files if 'L2' in x]
    # print(myplots.options[0])
    # myplots.set_data1(myplots.options[0])
    # myplots.set_data2(myplots.options[-4])
    # fig = myplots.return_volume(myplots.complete_list())
    # fig.show()
