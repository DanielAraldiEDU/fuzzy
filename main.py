import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import warnings
warnings.filterwarnings('ignore')

class CompleteFuzzyWeaponSystem:
    def __init__(self):
        self.setup_system()

    def create_fuzzy_variables(self):
        self.distance = ctrl.Antecedent(np.arange(0, 101, 1), 'distance')
        
        # Criar variáveis de munição separadas para cada arma
        self.ammo_rocket = ctrl.Antecedent(np.arange(0, 101, 1), 'ammo_rocket')
        self.ammo_rifle = ctrl.Antecedent(np.arange(0, 101, 1), 'ammo_rifle')
        self.ammo_pistol = ctrl.Antecedent(np.arange(0, 101, 1), 'ammo_pistol')
        
        # Consequentes separados para cada arma
        self.des_rocket = ctrl.Consequent(np.arange(0, 101, 1), 'des_rocket')
        self.des_rifle = ctrl.Consequent(np.arange(0, 101, 1), 'des_rifle')
        self.des_pistol = ctrl.Consequent(np.arange(0, 101, 1), 'des_pistol')

        # Funções de pertinência para distância
        self.distance['close'] = fuzz.trimf(self.distance.universe, [0, 0, 35])
        self.distance['medium'] = fuzz.trimf(self.distance.universe, [25, 50, 75])
        self.distance['far'] = fuzz.trimf(self.distance.universe, [65, 100, 100])

        # Funções de pertinência para munição do foguete
        self.ammo_rocket['low'] = fuzz.trimf(self.ammo_rocket.universe, [0, 0, 35])
        self.ammo_rocket['medium'] = fuzz.trimf(self.ammo_rocket.universe, [25, 50, 75])
        self.ammo_rocket['high'] = fuzz.trimf(self.ammo_rocket.universe, [65, 100, 100])

        # Funções de pertinência para munição do rifle
        self.ammo_rifle['low'] = fuzz.trimf(self.ammo_rifle.universe, [0, 0, 35])
        self.ammo_rifle['medium'] = fuzz.trimf(self.ammo_rifle.universe, [25, 50, 75])
        self.ammo_rifle['high'] = fuzz.trimf(self.ammo_rifle.universe, [65, 100, 100])

        # Funções de pertinência para munição da pistola
        self.ammo_pistol['low'] = fuzz.trimf(self.ammo_pistol.universe, [0, 0, 35])
        self.ammo_pistol['medium'] = fuzz.trimf(self.ammo_pistol.universe, [25, 50, 75])
        self.ammo_pistol['high'] = fuzz.trimf(self.ammo_pistol.universe, [65, 100, 100])

        # Funções de pertinência para desejabilidade do foguete
        self.des_rocket['undesirable'] = fuzz.trimf(self.des_rocket.universe, [0, 0, 40])
        self.des_rocket['desirable'] = fuzz.trimf(self.des_rocket.universe, [30, 50, 70])
        self.des_rocket['essential'] = fuzz.trimf(self.des_rocket.universe, [60, 100, 100])

        # Funções de pertinência para desejabilidade do rifle
        self.des_rifle['undesirable'] = fuzz.trimf(self.des_rifle.universe, [0, 0, 40])
        self.des_rifle['desirable'] = fuzz.trimf(self.des_rifle.universe, [30, 50, 70])
        self.des_rifle['essential'] = fuzz.trimf(self.des_rifle.universe, [60, 100, 100])

        # Funções de pertinência para desejabilidade da pistola
        self.des_pistol['undesirable'] = fuzz.trimf(self.des_pistol.universe, [0, 0, 40])
        self.des_pistol['desirable'] = fuzz.trimf(self.des_pistol.universe, [30, 50, 70])
        self.des_pistol['essential'] = fuzz.trimf(self.des_pistol.universe, [60, 100, 100])

    def create_rocket_launcher_system(self):
        rule1 = ctrl.Rule(self.distance['close'] & self.ammo_rocket['low'], self.des_rocket['undesirable'])
        rule2 = ctrl.Rule(self.distance['close'] & self.ammo_rocket['medium'], self.des_rocket['undesirable'])
        rule3 = ctrl.Rule(self.distance['close'] & self.ammo_rocket['high'], self.des_rocket['undesirable'])

        rule4 = ctrl.Rule(self.distance['medium'] & self.ammo_rocket['low'], self.des_rocket['undesirable'])
        rule5 = ctrl.Rule(self.distance['medium'] & self.ammo_rocket['medium'], self.des_rocket['desirable'])
        rule6 = ctrl.Rule(self.distance['medium'] & self.ammo_rocket['high'], self.des_rocket['essential'])

        rule7 = ctrl.Rule(self.distance['far'] & self.ammo_rocket['low'], self.des_rocket['undesirable'])
        rule8 = ctrl.Rule(self.distance['far'] & self.ammo_rocket['medium'], self.des_rocket['desirable'])
        rule9 = ctrl.Rule(self.distance['far'] & self.ammo_rocket['high'], self.des_rocket['essential'])

        system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        return ctrl.ControlSystemSimulation(system)

    def create_sniper_rifle_system(self):
        rule1 = ctrl.Rule(self.distance['close'] & self.ammo_rifle['low'], self.des_rifle['undesirable'])
        rule2 = ctrl.Rule(self.distance['close'] & self.ammo_rifle['medium'], self.des_rifle['undesirable'])
        rule3 = ctrl.Rule(self.distance['close'] & self.ammo_rifle['high'], self.des_rifle['undesirable'])

        rule4 = ctrl.Rule(self.distance['medium'] & self.ammo_rifle['low'], self.des_rifle['desirable'])
        rule5 = ctrl.Rule(self.distance['medium'] & self.ammo_rifle['medium'], self.des_rifle['desirable'])
        rule6 = ctrl.Rule(self.distance['medium'] & self.ammo_rifle['high'], self.des_rifle['essential'])

        rule7 = ctrl.Rule(self.distance['far'] & self.ammo_rifle['low'], self.des_rifle['essential'])
        rule8 = ctrl.Rule(self.distance['far'] & self.ammo_rifle['medium'], self.des_rifle['essential'])
        rule9 = ctrl.Rule(self.distance['far'] & self.ammo_rifle['high'], self.des_rifle['essential'])

        system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        return ctrl.ControlSystemSimulation(system)

    def create_pistol_system(self):
        rule1 = ctrl.Rule(self.distance['close'] & self.ammo_pistol['low'], self.des_pistol['desirable'])
        rule2 = ctrl.Rule(self.distance['close'] & self.ammo_pistol['medium'], self.des_pistol['essential'])
        rule3 = ctrl.Rule(self.distance['close'] & self.ammo_pistol['high'], self.des_pistol['essential'])

        rule4 = ctrl.Rule(self.distance['medium'] & self.ammo_pistol['low'], self.des_pistol['undesirable'])
        rule5 = ctrl.Rule(self.distance['medium'] & self.ammo_pistol['medium'], self.des_pistol['undesirable'])
        rule6 = ctrl.Rule(self.distance['medium'] & self.ammo_pistol['high'], self.des_pistol['desirable'])

        rule7 = ctrl.Rule(self.distance['far'] & self.ammo_pistol['low'], self.des_pistol['undesirable'])
        rule8 = ctrl.Rule(self.distance['far'] & self.ammo_pistol['medium'], self.des_pistol['undesirable'])
        rule9 = ctrl.Rule(self.distance['far'] & self.ammo_pistol['high'], self.des_pistol['undesirable'])

        system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        return ctrl.ControlSystemSimulation(system)

    def setup_system(self):
        self.create_fuzzy_variables()
        self.rocket_simulator = self.create_rocket_launcher_system()
        self.rifle_simulator = self.create_sniper_rifle_system()
        self.pistol_simulator = self.create_pistol_system()

        self.weapons = [
            ("Rocket Launcher", self.rocket_simulator, "#ff6b6b", 'ammo_rocket'),
            ("Sniper Rifle", self.rifle_simulator, "#4ecdc4", 'ammo_rifle'),
            ("Pistol", self.pistol_simulator, "#45b7d1", 'ammo_pistol')
        ]

    def evaluate_weapon(self, simulator, distance_val, ammunition_val, ammo_input_name):
        try:
            simulator.input['distance'] = distance_val
            simulator.input[ammo_input_name] = ammunition_val
            simulator.compute()
            
            # Determinar o nome correto da saída baseado na arma
            if ammo_input_name == 'ammo_rocket':
                output_name = 'des_rocket'
            elif ammo_input_name == 'ammo_rifle':
                output_name = 'des_rifle'
            else:  # ammo_pistol
                output_name = 'des_pistol'
            
            return simulator.output[output_name]
        except Exception as e:
            print(f"⚠️ Erro ao avaliar arma: {e}")
            return 0.0

    def evaluate_all_weapons(self, distance_val, ammo_values):
        results = {}

        for weapon_name, simulator, color, ammo_input in self.weapons:
            score = self.evaluate_weapon(simulator, distance_val, ammo_values[weapon_name], ammo_input)
            results[weapon_name] = {
                'score': score,
                'color': color,
                'ammunition': ammo_values[weapon_name]
            }

        best_weapon = max(results.keys(), key=lambda x: results[x]['score'])
        return results, best_weapon

    def get_user_input_single(self):
        print("\n" + "="*60)
        print("📝 ENTRADA DE DADOS - TESTE ÚNICO")
        print("="*60)

        while True:
            try:
                print("\n🎯 Insira os dados do cenário de combate:")
                distance = float(input("📏 Distância do alvo (0-100%): "))
                
                if not (0 <= distance <= 100):
                    print("❌ ERRO: Distância deve estar entre 0 e 100!")
                    continue
                
                print("\n🔫 Munição disponível para cada arma:")
                ammo_rocket = float(input("  🚀 Rocket Launcher (0-100%): "))
                ammo_rifle = float(input("  🎯 Sniper Rifle (0-100%): "))
                ammo_pistol = float(input("  🔫 Pistol (0-100%): "))

                if not all(0 <= ammo <= 100 for ammo in [ammo_rocket, ammo_rifle, ammo_pistol]):
                    print("❌ ERRO: Todas as munições devem estar entre 0 e 100!")
                    continue

                ammo_values = {
                    "Rocket Launcher": ammo_rocket,
                    "Sniper Rifle": ammo_rifle,
                    "Pistol": ammo_pistol
                }

                return distance, ammo_values

            except ValueError:
                print("❌ ERRO: Digite apenas números válidos!")
            except KeyboardInterrupt:
                return None, None

    def get_user_input_multiple(self):
        print("\n" + "="*60)
        print("📝 ENTRADA DE DADOS - TESTES MÚLTIPLOS")
        print("="*60)

        test_cases = []

        while True:
            try:
                num_tests = int(input("\n🔢 Quantos cenários deseja testar? (1-10): "))
                if 1 <= num_tests <= 10:
                    break
                else:
                    print("❌ Digite um número entre 1 e 10!")
            except ValueError:
                print("❌ Digite um número válido!")

        for i in range(num_tests):
            print(f"\n--- Cenário {i+1} ---")
            while True:
                try:
                    distance = float(input(f"📏 Distância do alvo (0-100%): "))
                    
                    if not (0 <= distance <= 100):
                        print("❌ Distância deve estar entre 0 e 100!")
                        continue
                    
                    print("🔫 Munição disponível para cada arma:")
                    ammo_rocket = float(input("  🚀 Rocket Launcher (0-100%): "))
                    ammo_rifle = float(input("  🎯 Sniper Rifle (0-100%): "))
                    ammo_pistol = float(input("  🔫 Pistol (0-100%): "))

                    if not all(0 <= ammo <= 100 for ammo in [ammo_rocket, ammo_rifle, ammo_pistol]):
                        print("❌ Todas as munições devem estar entre 0 e 100!")
                        continue

                    description = input(f"📝 Descrição do cenário (opcional): ").strip()
                    if not description:
                        description = f"Cenário {i+1}"

                    test_cases.append({
                        'distance': distance,
                        'ammo_values': {
                            "Rocket Launcher": ammo_rocket,
                            "Sniper Rifle": ammo_rifle,
                            "Pistol": ammo_pistol
                        },
                        'description': description
                    })
                    break

                except ValueError:
                    print("❌ Digite apenas números válidos!")

        return test_cases

    def display_results_single(self, distance, ammo_values, results, best_weapon):
        print("\n" + "="*60)
        print("📊 RESULTADOS DA SIMULAÇÃO")
        print("="*60)

        print(f"\n🎯 CENÁRIO TESTADO:")
        print(f"   📏 Distância do alvo: {distance}%")
        print(f"\n   🔫 Munição disponível:")
        for weapon, ammo in ammo_values.items():
            print(f"      • {weapon}: {ammo}%")

        print(f"\n📈 DESEJABILIDADE DAS ARMAS:")
        print("-" * 40)

        sorted_results = sorted(results.items(), key=lambda x: x[1]['score'], reverse=True)

        for i, (weapon, data) in enumerate(sorted_results, 1):
            score = data['score']

            if score >= 60:
                classification = "ESSENCIAL"
                emoji = "🟢"
            elif score >= 30:
                classification = "DESEJÁVEL"
                emoji = "🟡"
            else:
                classification = "INDESEJÁVEL"
                emoji = "🔴"

            if weapon == best_weapon:
                print(f"🏆 {i}º {weapon}: {score:.2f}% - {classification} {emoji}")
            else:
                print(f"   {i}º {weapon}: {score:.2f}% - {classification} {emoji}")

        print(f"\n🎯 RECOMENDAÇÃO FINAL:")
        print(f"   ✅ Arma recomendada: {best_weapon}")
        print(f"   📊 Pontuação: {results[best_weapon]['score']:.2f}%")
        print(f"   🔫 Munição disponível: {results[best_weapon]['ammunition']:.2f}%")

    def display_results_multiple(self, test_cases, all_results):
        print("\n" + "="*80)
        print("📊 RESULTADOS DOS TESTES MÚLTIPLOS")
        print("="*80)

        for i, (case, (results, best_weapon)) in enumerate(zip(test_cases, all_results), 1):
            print(f"\n--- TESTE {i}: {case['description']} ---")
            print(f"📏 Distância: {case['distance']}%")
            print("🔫 Munição:")
            for weapon, ammo in case['ammo_values'].items():
                print(f"   • {weapon}: {ammo}%")
            
            print("\nResultados:")
            for weapon, data in results.items():
                score = data['score']
                marker = "👑" if weapon == best_weapon else "  "
                print(f"{marker} {weapon}: {score:.2f}%")

            print(f"🏆 Melhor: {best_weapon} ({results[best_weapon]['score']:.2f}%)")

    def plot_results(self, distance, ammo_values, results, best_weapon):
        try:
            weapons = list(results.keys())
            scores = [results[w]['score'] for w in weapons]
            colors = [results[w]['color'] for w in weapons]

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

            # Gráfico de desejabilidade
            bars = ax1.bar(weapons, scores, color=colors, alpha=0.8, edgecolor='black', linewidth=2)

            best_idx = weapons.index(best_weapon)
            bars[best_idx].set_alpha(1.0)
            bars[best_idx].set_linewidth(4)
            bars[best_idx].set_edgecolor('gold')

            for bar, score in zip(bars, scores):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                        f'{score:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)

            ax1.axhline(y=30, color='orange', linestyle='--', alpha=0.7, label='Limiar Desejável')
            ax1.axhline(y=60, color='green', linestyle='--', alpha=0.7, label='Limiar Essencial')

            ax1.set_title(f'Desejabilidade das Armas\nDistância: {distance}%', 
                         fontsize=14, fontweight='bold')
            ax1.set_ylabel('Desejabilidade (%)', fontsize=12)
            ax1.set_xlabel('Armas Disponíveis', fontsize=12)
            ax1.set_ylim(0, 110)
            ax1.legend()
            ax1.grid(True, alpha=0.3, axis='y')

            # Gráfico de munição disponível
            ammo_list = [ammo_values[w] for w in weapons]
            bars2 = ax2.bar(weapons, ammo_list, color=colors, alpha=0.6, edgecolor='black', linewidth=2)

            for bar, ammo in zip(bars2, ammo_list):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                        f'{ammo:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)

            ax2.set_title('Munição Disponível por Arma', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Munição (%)', fontsize=12)
            ax2.set_xlabel('Armas Disponíveis', fontsize=12)
            ax2.set_ylim(0, 110)
            ax2.grid(True, alpha=0.3, axis='y')

            plt.suptitle('Sistema Fuzzy - Seleção de Armas NPC (Munição Individual)', 
                        fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"⚠️ Não foi possível exibir o gráfico: {e}")

    def show_menu(self):
        print("\n" + "="*80)
        print("🎮 SISTEMA FUZZY COMPLETO - SELEÇÃO DE ARMAS NPC")
        print("   (Com munição individual por arma)")
        print("="*80)
        print("Escolha uma opção:")
        print("1️⃣  Teste único (entrada manual)")
        print("2️⃣  Testes múltiplos (vários cenários)")
        print("0️⃣  Sair")
        print("-" * 80)

    def run(self):
        while True:
            try:
                self.show_menu()
                choice = input("Digite sua escolha (0-2): ").strip()

                if choice == '0':
                    print("\n👋 Obrigado por usar o Sistema Fuzzy Completo!")
                    break

                elif choice == '1':
                    distance, ammo_values = self.get_user_input_single()
                    if distance is not None:
                        results, best_weapon = self.evaluate_all_weapons(distance, ammo_values)
                        self.display_results_single(distance, ammo_values, results, best_weapon)

                        show_graph = input("\n📊 Deseja ver o gráfico dos resultados? (s/n): ").lower().strip()
                        if show_graph == 's':
                            self.plot_results(distance, ammo_values, results, best_weapon)

                elif choice == '2':
                    test_cases = self.get_user_input_multiple()
                    if test_cases:
                        all_results = []
                        for case in test_cases:
                            results, best_weapon = self.evaluate_all_weapons(case['distance'], case['ammo_values'])
                            all_results.append((results, best_weapon))

                        self.display_results_multiple(test_cases, all_results)

                else:
                    print("❌ Opção inválida! Digite um número de 0 a 2.")

                if choice != '0':
                    input("\n⏸️  Pressione ENTER para continuar...")

            except KeyboardInterrupt:
                print("\n\n👋 Sistema encerrado pelo usuário.")
                break
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
                input("⏸️  Pressione ENTER para continuar...")

def main():
    system = CompleteFuzzyWeaponSystem()
    system.run()

if __name__ == "__main__":
    main()
