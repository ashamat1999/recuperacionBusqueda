import requests
import bs4
import re

from app.scraper.search_engines import Google, Yahoo, Bing

class Selector:
    palabras_buscar=[]
    metodos = []
    frecuencias = []
    pesos = []
    indices_0 = []
    indices_1 = []
    lista_final = []


    def __init__(self, query, cant_documentos, google_chkbx, yahoo_chkbx) -> None:
        self.query = query
        self.cant_documentos = cant_documentos
        self.google_chkbx = google_chkbx
        self.yahoo_chkbx = yahoo_chkbx
        self.frecuencias = []
        self.lista_final = []

        pass

    def seleccionar_motores(self):
        self.motores = []
        if self.google_chkbx == '1':
            self.motores.append('google')
        
        if self.yahoo_chkbx == '1':
            self.motores.append('yahoo')
            
        return self.motores
    
    

    def proccess_query(self, query, motor):
        print('Query ->:', query)
        print('Motor ->:', motor)
        
        self.palabras_buscar.append(query)
        
        return query
    
    def seleccionar_documentos(self):

        google_engine = Google()
        yahoo_engine = Yahoo()

        dict_motores = {'google': google_engine, 'yahoo':yahoo_engine}

        self.links = []
        self.texto = []
        self.hosts = []

        for motor in self.motores:
            q = self.query
            proccessed_query = self.proccess_query(q, motor)
            print("Searching...")
            results = dict_motores[motor].search(proccessed_query, pages=1)
            self.links.append(results.links())
            self.texto.append(results.text())
            self.hosts.append(results.hosts())
        
        print(self.links)
        return self.links
    
    
    def query_dispatch(self):
        
        for links_motor in self.links:
            prov_array = []
            for link in links_motor:
                print(link)
                freq = 0
                try:
                    data = requests.get(link)
                    print(data)
                    soup = bs4.BeautifulSoup(data.text, 'html.parser')
                    
                    if not self.metodos:
                        if soup.body is not None:
                            results = soup.body.find_all(string=re.compile('.*{0}.*'.format(self.palabras_buscar[0])), recursive=True)
                            #print ('Found the word "{0}" {1} times\n'.format(self.palabras_buscar[0], len(results)))
                            freq = len(results)
                            print(freq)
                            prov_array.append(freq)
                        else:
                            prov_array.append(freq)
                except:
                    prov_array.append(freq)
            
            self.frecuencias.append(prov_array)

        return self.frecuencias
    
    

    def results_mixer(self):
        self.cant_documentos = int(self.cant_documentos)
        indices_eliminar_0 = []
        indices_eliminar_1 = []
        # Verificar links en común, sumar peso

        prov_links_0 = self.links
        prov_host_0 = self.hosts
        prov_freq_0 = self.frecuencias

        if len(self.motores) > 1:
            for host in self.hosts[0]:
                if host in self.hosts[1]:
                    index_host = prov_host_0[0].index(host)
                    index_host_1 = self.hosts[1].index(host)
                    print(prov_freq_0[0], index_host)

                    doc = ( self.motores[0], self.motores[1], prov_links_0[0][index_host])
                    
                    prov_links_0[0].pop(index_host)
                    prov_host_0[0].pop(index_host)
                    prov_freq_0[0].pop(index_host)

                    prov_links_0[1].pop(index_host_1)
                    prov_host_0[1].pop(index_host_1)
                    prov_freq_0[1].pop(index_host_1)

                    self.cant_documentos -= 1
                    self.lista_final.append(doc)

            last_index = len(self.links[0])
            prov_links = prov_links_0[0] + prov_links_0[1]
            prov_freq = prov_freq_0[0] + prov_freq_0[1]

            result = []

            for x in range(self.cant_documentos):  # Número de veces que ejecutamos este bucle
                maximo = max(prov_freq)  # Buscamos el máximo valor
                index = prov_freq.index(maximo)
                if index >= last_index:
                    doc = ( self.motores[1], prov_links[index])
                    self.lista_final.append(doc)
                else:
                    doc = ( self.motores[0], prov_links[index])
                    self.lista_final.append(doc)

                prov_freq.remove(maximo)  # Lo eliminamos de la lista antigua, para que el próximo "máximo valor" no incluya este valor
                prov_links.pop(index)


        else:
            prov_links_0 = self.links
            prov_host_0 = self.hosts
            prov_freq_0 = self.frecuencias

            last_index = len(self.links[0])
            prov_links = prov_links_0[0] 
            prov_freq = prov_freq_0[0] 

            for x in range(self.cant_documentos):  # Número de veces que ejecutamos este bucle
                maximo = max(prov_freq)  # Buscamos el máximo valor
                index = prov_freq.index(maximo)
                doc = ( self.motores[0], prov_links[index])
                self.lista_final.append(doc)

                prov_freq.remove(maximo)  # Lo eliminamos de la lista antigua, para que el próximo "máximo valor" no incluya este valor
                prov_links.pop(index)

        return self.lista_final
    
    def get_req_docs(self, links, freq):
        result = []
        for x in range(self.cant_documentos):  # Número de veces que ejecutamos este bucle
            maximo = max(freq)  # Buscamos el máximo valor
            index = freq.index(maximo)
            result.append(index)  # Lo añadimos a una nueva lista
            freq.remove(maximo)  # Lo eliminamos de la lista antigua, para que el próximo "máximo valor" no incluya este valor

        print('indices top ->: ', result)
        return result
    
    
    