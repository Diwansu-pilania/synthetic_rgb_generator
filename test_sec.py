from scenario_controller import ScenarioController


controller = ScenarioController()

for i in range(10):

    scenario = controller.generate_scenario()

    print(f"\n========== Scenario {i + 1} ==========")

    print(scenario.model_dump_json(indent=2))