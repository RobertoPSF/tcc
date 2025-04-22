import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import sys
import glob
from collections import Counter
from report_generator import ReportGenerator
import io

class KeyloggerAnalyzer:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = None
        self.load_data()
        
    def load_data(self):
        """Carrega os dados do arquivo JSON"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"Dados carregados com sucesso: {len(self.data)} eventos registrados.")
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")
            sys.exit(1)
    
    def calculate_typing_metrics(self):
        """Calcula métricas de digitação"""
        # Filtra apenas eventos com hold_time e flight_time
        valid_events = [event for event in self.data if 'hold_time' in event and event['hold_time'] is not None]
        
        if not valid_events:
            return {
                "hold_time_avg": 0,
                "hold_time_std": 0,
                "flight_time_avg": 0,
                "flight_time_std": 0,
                "total_events": 0
            }
        
        # Extrai hold_time e flight_time
        hold_times = [event['hold_time'] for event in valid_events if event['hold_time'] is not None]
        flight_times = [event['flight_time'] for event in valid_events if event['flight_time'] is not None]
        
        # Calcula médias e desvios padrão
        hold_time_avg = np.mean(hold_times) if hold_times else 0
        hold_time_std = np.std(hold_times) if hold_times else 0
        flight_time_avg = np.mean(flight_times) if flight_times else 0
        flight_time_std = np.std(flight_times) if flight_times else 0
        
        return {
            "hold_time_avg": round(hold_time_avg, 3),
            "hold_time_std": round(hold_time_std, 3),
            "flight_time_avg": round(flight_time_avg, 3),
            "flight_time_std": round(flight_time_std, 3),
            "total_events": len(valid_events)
        }
    
    def analyze_suspicious_commands(self):
        """Analisa a frequência de comandos suspeitos"""
        # Comandos considerados suspeitos
        suspicious_commands = ["paste", "copy", "cut"]
        
        # Conta a ocorrência de cada comando
        command_counts = Counter()
        for event in self.data:
            if event.get('command_type') in suspicious_commands:
                command_counts[event['command_type']] += 1
        
        # Calcula a porcentagem de comandos suspeitos
        total_commands = sum(command_counts.values())
        total_events = len(self.data)
        suspicious_percentage = (total_commands / total_events * 100) if total_events > 0 else 0
        
        return {
            "command_counts": dict(command_counts),
            "suspicious_percentage": round(suspicious_percentage, 2),
            "total_commands": total_commands
        }
    
    def calculate_manhattan_distance(self):
        """Calcula a distância de Manhattan para avaliar o padrão comportamental"""
        # Agrupa eventos por aplicação
        app_events = {}
        for event in self.data:
            app = event.get('application', 'Unknown')
            if app not in app_events:
                app_events[app] = []
            app_events[app].append(event)
        
        # Calcula métricas por aplicação
        app_metrics = {}
        for app, events in app_events.items():
            # Calcula tempo total gasto em cada aplicação
            if len(events) >= 2:
                start_time = datetime.strptime(events[0]['timestamp'], "%Y-%m-%d %H:%M:%S")
                end_time = datetime.strptime(events[-1]['timestamp'], "%Y-%m-%d %H:%M:%S")
                duration = (end_time - start_time).total_seconds()
                
                # Calcula taxa de digitação (eventos por segundo)
                typing_rate = len(events) / duration if duration > 0 else 0
                
                # Calcula porcentagem de comandos suspeitos
                suspicious_count = sum(1 for e in events if e.get('command_type') in ["paste", "copy", "cut"])
                suspicious_ratio = suspicious_count / len(events) if len(events) > 0 else 0
                
                app_metrics[app] = {
                    "duration": round(duration, 2),
                    "typing_rate": round(typing_rate, 2),
                    "suspicious_ratio": round(suspicious_ratio, 2),
                    "event_count": len(events)
                }
        
        return app_metrics
    
    def generate_report(self):
        """Gera um relatório completo da análise"""
        typing_metrics = self.calculate_typing_metrics()
        suspicious_analysis = self.analyze_suspicious_commands()
        manhattan_metrics = self.calculate_manhattan_distance()
        
        # Determina se o comportamento é suspeito
        is_suspicious = False
        suspicious_reasons = []
        
        # Critérios para considerar suspeito
        if suspicious_analysis["suspicious_percentage"] > 15:
            is_suspicious = True
            suspicious_reasons.append(f"Alta porcentagem de comandos suspeitos: {suspicious_analysis['suspicious_percentage']}%")
        
        # Verifica padrões de digitação anormais
        if typing_metrics["hold_time_std"] > 0.2 or typing_metrics["flight_time_std"] > 0.3:
            is_suspicious = True
            suspicious_reasons.append("Padrão de digitação irregular (alta variabilidade)")
        
        # Verifica se há muitas mudanças de aplicação
        if len(manhattan_metrics) > 5:
            is_suspicious = True
            suspicious_reasons.append(f"Muitas aplicações diferentes utilizadas: {len(manhattan_metrics)}")
        
        # Gera o relatório
        report = {
            "file_analyzed": self.json_file,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "typing_metrics": typing_metrics,
            "suspicious_commands": suspicious_analysis,
            "application_metrics": manhattan_metrics,
            "is_suspicious": is_suspicious,
            "suspicious_reasons": suspicious_reasons,
            "conclusion": "ATENÇÃO NECESSÁRIA" if is_suspicious else "COMPORTAMENTO NORMAL"
        }
        
        return report
    
    def plot_typing_patterns(self):
        """Gera gráficos de padrões de digitação e retorna como bytes"""
        # Extrai dados para plotagem
        hold_times = [event['hold_time'] for event in self.data if 'hold_time' in event and event['hold_time'] is not None]
        flight_times = [event['flight_time'] for event in self.data if 'flight_time' in event and event['flight_time'] is not None]
        
        # Cria figura com subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Plot de hold times
        if hold_times:
            ax1.hist(hold_times, bins=30, alpha=0.7, color='blue')
            ax1.set_title('Distribuição de Tempos de Pressionamento (Hold Time)')
            ax1.set_xlabel('Tempo (segundos)')
            ax1.set_ylabel('Frequência')
        
        # Plot de flight times
        if flight_times:
            ax2.hist(flight_times, bins=30, alpha=0.7, color='green')
            ax2.set_title('Distribuição de Tempos Entre Teclas (Flight Time)')
            ax2.set_xlabel('Tempo (segundos)')
            ax2.set_ylabel('Frequência')
        
        plt.tight_layout()
        
        # Salva o gráfico em um buffer de memória
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def generate_pdf_report(self, report, output_file="analysis_report.pdf"):
        """Gera um relatório em PDF"""
        # Gera os gráficos e adiciona ao relatório
        graph_data = self.plot_typing_patterns()
        report['graph_data'] = graph_data
        
        generator = ReportGenerator(report, output_file)
        return generator.generate_pdf()

def process_json_files(input_path, output_dir):
    """Processa arquivos JSON (seja um arquivo único ou um diretório com múltiplos arquivos)"""
    # Verifica se o caminho de entrada existe
    if not os.path.exists(input_path):
        print(f"Caminho não encontrado: {input_path}")
        sys.exit(1)
    
    # Cria o diretório de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Diretório de saída criado: {output_dir}")
    
    # Determina se o caminho é um arquivo ou diretório
    if os.path.isfile(input_path):
        # Se for um arquivo, verifica se é JSON
        if input_path.endswith('.json'):
            json_files = [input_path]
            input_dir = os.path.dirname(input_path)
        else:
            print(f"O arquivo {input_path} não é um arquivo JSON")
            sys.exit(1)
    else:
        # Se for um diretório, encontra todos os arquivos JSON
        input_dir = input_path
        all_files = os.listdir(input_dir)
        json_files = [os.path.join(input_dir, f) for f in all_files 
                     if f.endswith('.json') and os.path.isfile(os.path.join(input_dir, f))]
    
    if not json_files:
        print(f"Nenhum arquivo JSON encontrado em: {input_path}")
        sys.exit(1)
    
    print(f"Encontrados {len(json_files)} arquivo(s) JSON para análise\n")
    
    # Processa cada arquivo JSON
    for json_file_path in json_files:
        try:
            # Extrai o nome do arquivo sem a extensão para usar no nome do relatório
            json_file_name = os.path.basename(json_file_path)
            file_name_without_ext = os.path.splitext(json_file_name)[0]
            
            # Define o caminho do arquivo de saída
            output_file = os.path.join(output_dir, f"{file_name_without_ext}_report.pdf")
            
            print(f"Processando arquivo: {json_file_name}")
            
            # Cria o analisador e gera o relatório
            analyzer = KeyloggerAnalyzer(json_file_path)
            report = analyzer.generate_report()
            
            # Gera o relatório PDF
            analyzer.generate_pdf_report(report, output_file)
            
            # Exibe resumo do relatório
            print(f"\n===== RESUMO DA ANÁLISE: {json_file_name} =====")
            print(f"Arquivo analisado: {report['file_analyzed']}")
            print(f"Data da análise: {report['analysis_date']}")
            print(f"Total de eventos: {report['typing_metrics']['total_events']}")
            print(f"Tempo médio de pressionamento: {report['typing_metrics']['hold_time_avg']} segundos")
            print(f"Tempo médio entre teclas: {report['typing_metrics']['flight_time_avg']} segundos")
            print(f"Porcentagem de comandos suspeitos: {report['suspicious_commands']['suspicious_percentage']}%")
            
            if report['is_suspicious']:
                print("\nRazões para suspeita:")
                for reason in report['suspicious_reasons']:
                    print(f"- {reason}")
            
            print(f"\nRelatório PDF gerado com sucesso em: {output_file}\n")
            
        except Exception as e:
            print(f"Erro ao processar o arquivo {json_file_name}: {e}")
            continue
    
    print("Processo concluído! Todos os arquivos foram analisados.")

def main():
    if len(sys.argv) < 2:
        print("Uso: python analyzer.py arquivo_ou_diretorio")
        print("     python analyzer.py arquivo.json")
        print("     python analyzer.py diretorio/")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_dir = "output"
    
    process_json_files(input_path, output_dir)

if __name__ == "__main__":
    main()