import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

plt.ioff()

def pdf(sales, top10_searches, bottom10_searches, top5_scores, bottom5_scores, meses, anuales, mes):
  pp = PdfPages("Reporte.pdf")

  # Pagina 1: 5 productos con mas ventas
  pag_1, ((tab1, ax1), (tab2, ax2), (tab3, ax3)) = plt.subplots(3, 2, figsize=(9, 14), gridspec_kw={'width_ratios': [2, 1]})
  tab = [tab1, tab2, tab3]
  ax = [ax1, ax2, ax3]
  pag_1.suptitle("Los 5 productos con mayores ventas en los ultimos 3 meses")
  for count, mes_anio in enumerate(sales['Mes_anio'].sort_values().unique()[-3:]):
    top5_sales = sales[sales['Mes_anio'] == mes_anio].groupby('Nombre').agg(Ventas=('Precio', 'size'), Ingreso=('Precio', 'sum')).sort_values(by='Ventas', ascending=False).head()
    tab[count].table(cellText=top5_sales.values, colLabels=top5_sales.columns, rowLabels=top5_sales.index.str[:15], loc='center',
    colColours=np.full(len(top5_sales.columns), fill_value='#d9d9d9'))
    tab[count].axis('off')
    tab[count].set_title(f"{pd.to_datetime(mes_anio).strftime('%B %Y')}", x=0.5)
    squarify.plot(sizes=top5_sales['Ventas'], label=(top5_sales.index.str[:5] + ' ' + top5_sales['Ventas'].astype(str)), ax=ax[count])
    ax[count].axis('off')

  pp.savefig(pag_1 ,bbox_inches='tight')

  # Pagina 2: 10 productos con mas busquedas
  pag_2, (tab, ax) = plt.subplots(2, 1, figsize=(9, 9))
  pag_2.suptitle("Los 10 productos con mas busquedas")
  tab.table(cellText=top10_searches.values, colLabels=top10_searches.columns, rowLabels=top10_searches.index.str[:15], loc='center', colColours=np.full(len(top10_searches.columns), fill_value='#d9d9d9'))
  tab.axis('off')
  top10_searches.index = top10_searches.index.str[:5]
  sns.barplot(data=top10_searches.reset_index(), x='Nombre', y='Busquedas', ax=ax)

  pp.savefig(pag_2 ,bbox_inches='tight')

  # Pagina 3: 5 productos con mas ventas
  pag_3, ((tab1, ax1), (tab2, ax2), (tab3, ax3)) = plt.subplots(3, 2, figsize=(9, 14), gridspec_kw={'width_ratios': [2, 1]})
  tab = [tab1, tab2, tab3]
  ax = [ax1, ax2, ax3]
  pag_3.suptitle("Los 5 productos con menores ventas en los ultimos 3 meses")
  for count, mes_anio in enumerate(sales['Mes_anio'].sort_values().unique()[-3:]):
    bottom5_sales = sales[sales['Mes_anio'] == mes_anio].groupby('Nombre').agg(Ventas=('Precio', 'size'), Ingreso=('Precio', 'sum')).sort_values(by='Ventas').head()
    tab[count].table(cellText=bottom5_sales.values, colLabels=bottom5_sales.columns, rowLabels=bottom5_sales.index.str[:15], loc='center',
    colColours=np.full(len(bottom5_sales.columns), fill_value='#d9d9d9'))
    tab[count].axis('off')
    tab[count].set_title(f"{pd.to_datetime(mes_anio).strftime('%B %Y')}", x=0.5)
    squarify.plot(sizes=bottom5_sales['Ventas'], label=(bottom5_sales.index.str[:5] + ' ' + bottom5_sales['Ventas'].astype(str)), ax=ax[count])
    ax[count].axis('off')

  pp.savefig(pag_3 ,bbox_inches='tight')

  # Pagina 4: 10 productos con menos busquedas
  pag_4, (tab, ax) = plt.subplots(2, 1, figsize=(9, 9))
  pag_4.suptitle("Los 10 productos con menos busquedas")
  tab.table(cellText=bottom10_searches.values, colLabels=bottom10_searches.columns, rowLabels=bottom10_searches.index.str[:15], loc='center', colColours=np.full(len(bottom10_searches.columns), fill_value='#d9d9d9'))
  tab.axis('off')
  bottom10_searches.index = bottom10_searches.index.str[:5]
  sns.barplot(data=bottom10_searches.reset_index(), x='Nombre', y='Busquedas', ax=ax)

  pp.savefig(pag_4 ,bbox_inches='tight')

  # Pagina 4: 5 productos con mejores y peores resenias
  pag_5, (tab1, tab2) = plt.subplots(2, 1, figsize=(9, 5))
  pag_5.suptitle("Resenias")
  tab1.table(cellText=top5_scores.values, colLabels=top5_scores.columns, rowLabels=top5_scores.index.str[:15], loc='center', colColours=np.full(len(top5_scores.columns), fill_value='#d9d9d9'))
  tab1.axis('off')
  tab1.set_title("Los productos mas vendidos y buscados con mejores resenias en promedio")
  tab2.table(cellText=bottom5_scores.values, colLabels=bottom5_scores.columns, rowLabels=bottom5_scores.index.str[:15], loc='center', colColours=np.full(len(bottom5_scores.columns), fill_value='#d9d9d9'))
  tab2.axis('off')
  tab1.set_title("Los productos menos vendidos y buscados con peores resenias en promedio")

  pp.savefig(pag_5 ,bbox_inches='tight')


  pp.close()
  
    
    