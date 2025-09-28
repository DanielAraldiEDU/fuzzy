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
        self.ammunition = ctrl.Antecedent(np.arange(0, 101, 1), 'ammunition')
        self.desirability = ctrl.Consequent(np.arange(0, 101, 1), 'desirability')

        self.distance['close'] = fuzz.trimf(self.distance.universe, [0, 0, 35])
        self.distance['medium'] = fuzz.trimf(self.distance.universe, [25, 50, 75])
        self.distance['far'] = fuzz.trimf(self.distance.universe, [65, 100, 100])

        self.ammunition['low'] = fuzz.trimf(self.ammunition.universe, [0, 0, 35])
        self.ammunition['medium'] = fuzz.trimf(self.ammunition.universe, [25, 50, 75])
        self.ammunition['high'] = fuzz.trimf(self.ammunition.universe, [65, 100, 100])

        self.desirability['undesirable'] = fuzz.trimf(self.desirability.universe, [0, 0, 40])
        self.desirability['desirable'] = fuzz.trimf(self.desirability.universe, [30, 50, 70])
        self.desirability['essential'] = fuzz.trimf(self.desirability.universe, [60, 100, 100])

    def create_rocket_launcher_system(self):
        rule1 = ctrl.Rule(self.distance['close'] & self.ammunition['low'], self.desirability['undesirable'])
        rule2 = ctrl.Rule(self.distance['close'] & self.ammunition['medium'], self.desirability['undesirable'])
        rule3 = ctrl.Rule(self.distance['close'] & self.ammunition['high'], self.desirability['undesirable'])

        rule4 = ctrl.Rule(self.distance['medium'] & self.ammunition['low'], self.desirability['undesirable'])
        rule5 = ctrl.Rule(self.distance['medium'] & self.ammunition['medium'], self.desirability['desirable'])
        rule6 = ctrl.Rule(self.distance['medium'] & self.ammunition['high'], self.desirability['essential'])

        rule7 = ctrl.Rule(self.distance['far'] & self.ammunition['low'], self.desirability['undesirable'])
        rule8 = ctrl.Rule(self.distance['far'] & self.ammunition['medium'], self.desirability['desirable'])
        rule9 = ctrl.Rule(self.distance['far'] & self.ammunition['high'], self.desirability['essential'])

        system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        return ctrl.ControlSystemSimulation(system)

    def create_sniper_rifle_system(self):

        rule1 = ctrl.Rule(self.distance['close'] & self.ammunition['low'], self.desirability['undesirable'])
        rule2 = ctrl.Rule(self.distance['close'] & self.ammunition['medium'], self.desirability['undesirable'])
        rule3 = ctrl.Rule(self.distance['close'] & self.ammunition['high'], self.desirability['undesirable'])

        rule4 = ctrl.Rule(self.distance['medium'] & self.ammunition['low'], self.desirability['desirable'])
        rule5 = ctrl.Rule(self.distance['medium'] & self.ammunition['medium'], self.desirability['desirable'])
        rule6 = ctrl.Rule(self.distance['medium'] & self.ammunition['high'], self.desirability['essential'])

        rule7 = ctrl.Rule(self.distance['far'] & self.ammunition['low'], self.desirability['essential'])
        rule8 = ctrl.Rule(self.distance['far'] & self.ammunition['medium'], self.desirability['essential'])
        rule9 = ctrl.Rule(self.distance['far'] & self.ammunition['high'], self.desirability['essential'])

        system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        return ctrl.ControlSystemSimulation(system)

    def create_pistol_system(self):
        rule1 = ctrl.Rule(self.distance['close'] & self.ammunition['low'], self.desirability['desirable'])
        rule2 = ctrl.Rule(self.distance['close'] & self.ammunition['medium'], self.desirability['essential'])
        rule3 = ctrl.Rule(self.distance['close'] & self.ammunition['high'], self.desirability['essential'])

        rule4 = ctrl.Rule(self.distance['medium'] & self.ammunition['low'], self.desirability['undesirable'])
        rule5 = ctrl.Rule(self.distance['medium'] & self.ammunition['medium'], self.desirability['undesirable'])
        rule6 = ctrl.Rule(self.distance['medium'] & self.ammunition['high'], self.desirability['desirable'])

        rule7 = ctrl.Rule(self.distance['far'] & self.ammunition['low'], self.desirability['undesirable'])
        rule8 = ctrl.Rule(self.distance['far'] & self.ammunition['medium'], self.desirability['undesirable'])
        rule9 = ctrl.Rule(self.distance['far'] & self.ammunition['high'], self.desirability['undesirable'])

        system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        return ctrl.ControlSystemSimulation(system)

    def setup_system(self):
        self.create_fuzzy_variables()
        self.rocket_simulator = self.create_rocket_launcher_system()
        self.rifle_simulator = self.create_sniper_rifle_system()
        self.pistol_simulator = self.create_pistol_system()

        self.weapons = [
            ("Rocket Launcher", self.rocket_simulator, "#ff6b6b"),
            ("Sniper Rifle", self.rifle_simulator, "#4ecdc4"),
            ("Pistol", self.pistol_simulator, "#45b7d1")
        ]

    def evaluate_weapon(self, simulator, distance_val, ammunition_val):
        try:
            simulator.input['distance'] = distance_val
            simulator.input['ammunition'] = ammunition_val
            simulator.compute()
            return simulator.output['desirability']
        except Exception as e:
            print(f"⚠️ Erro ao avaliar arma: {e}")
            return 0.0

    def evaluate_all_weapons(self, distance_val, ammunition_val):
        results = {}

        for weapon_name, simulator, color in self.weapons:
            score = self.evaluate_weapon(simulator, distance_val, ammunition_val)
            results[weapon_name] = {
                'score': score,
                'color': color
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
                ammunition = float(input("🔫 Quantidade de munição disponível (0-100%): "))

                if not (0 <= distance <= 100) or not (0 <= ammunition <= 100):
                    print("❌ ERRO: Valores devem estar entre 0 e 100!")
                    continue

                return distance, ammunition

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
                    ammunition = float(input(f"🔫 Munição disponível (0-100%): "))

                    if not (0 <= distance <= 100) or not (0 <= ammunition <= 100):
                        print("❌ Valores devem estar entre 0 e 100!")
                        continue

                    description = input(f"📝 Descrição do cenário (opcional): ").strip()
                    if not description:
                        description = f"Cenário {i+1}"

                    test_cases.append({
                        'distance': distance,
                        'ammunition': ammunition,
                        'description': description
                    })
                    break

                except ValueError:
                    print("❌ Digite apenas números válidos!")

        return test_cases

    def display_results_single(self, distance, ammunition, results, best_weapon):
        print("\n" + "="*60)
        print("📊 RESULTADOS DA SIMULAÇÃO")
        print("="*60)

        print(f"\n🎯 CENÁRIO TESTADO:")
        print(f"   📏 Distância do alvo: {distance}%")
        print(f"   🔫 Munição disponível: {ammunition}%")

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

    def display_results_multiple(self, test_cases, all_results):
        print("\n" + "="*80)
        print("📊 RESULTADOS DOS TESTES MÚLTIPLOS")
        print("="*80)

        for i, (case, (results, best_weapon)) in enumerate(zip(test_cases, all_results), 1):
            print(f"\n--- TESTE {i}: {case['description']} ---")
            print(f"📏 Distância: {case['distance']}% | 🔫 Munição: {case['ammunition']}%")
            print("Resultados:")

            for weapon, data in results.items():
                score = data['score']
                marker = "👑" if weapon == best_weapon else "  "
                print(f"{marker} {weapon}: {score:.2f}%")

            print(f"🏆 Melhor: {best_weapon} ({results[best_weapon]['score']:.2f}%)")

    def plot_results(self, distance, ammunition, results, best_weapon):
        try:
            weapons = list(results.keys())
            scores = [results[w]['score'] for w in weapons]
            colors = [results[w]['color'] for w in weapons]

            plt.figure(figsize=(12, 8))

            bars = plt.bar(weapons, scores, color=colors, alpha=0.8, edgecolor='black', linewidth=2)

            best_idx = weapons.index(best_weapon)
            bars[best_idx].set_alpha(1.0)
            bars[best_idx].set_linewidth(4)
            bars[best_idx].set_edgecolor('gold')

            for bar, score in zip(bars, scores):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                        f'{score:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)

            plt.axhline(y=30, color='orange', linestyle='--', alpha=0.7, label='Limiar Desejável')
            plt.axhline(y=60, color='green', linestyle='--', alpha=0.7, label='Limiar Essencial')

            plt.title(f'Sistema Fuzzy COMPLETO - Seleção de Armas NPC\nDistância: {distance}% | Munição: {ammunition}%', 
                     fontsize=16, fontweight='bold', pad=20)
            plt.ylabel('Desejabilidade (%)', fontsize=12)
            plt.xlabel('Armas Disponíveis', fontsize=12)
            plt.ylim(0, 110)
            plt.legend()
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"⚠️ Não foi possível exibir o gráfico: {e}")

    def show_menu(self):
        print("\n" + "="*80)
        print("🎮 SISTEMA FUZZY COMPLETO - SELEÇÃO DE ARMAS NPC")
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
                    distance, ammunition = self.get_user_input_single()
                    if distance is not None:
                        results, best_weapon = self.evaluate_all_weapons(distance, ammunition)
                        self.display_results_single(distance, ammunition, results, best_weapon)

                        show_graph = input("\n📊 Deseja ver o gráfico dos resultados? (s/n): ").lower().strip()
                        if show_graph == 's':
                            self.plot_results(distance, ammunition, results, best_weapon)

                elif choice == '2':
                    test_cases = self.get_user_input_multiple()
                    if test_cases:
                        all_results = []
                        for case in test_cases:
                            results, best_weapon = self.evaluate_all_weapons(case['distance'], case['ammunition'])
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
