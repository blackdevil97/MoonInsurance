import requests

def test_agent_service():
    response = requests.get("http://mooninsurance.local/agent")
    assert response.status_code == 200

def test_integration_service():
    response = requests.get("http://mooninsurance.local/sales")
    assert response.status_code == 200

def test_notification_service():
    response = requests.get("http://mooninsurance.local/notification/check_target/AGENT001")
    assert response.status_code == 200

def test_aggregator_service_best_teams():
    response = requests.get("http://mooninsurance.local/aggregation/best_teams")
    assert response.status_code == 200

def test_redshift_service_sync():
    response = requests.post("http://mooninsurance.local/sync/appointments_per_doctor")
    assert response.status_code == 200

if __name__ == "__main__":
    test_agent_service()
    test_integration_service()
    test_notification_service()
    test_aggregator_service_best_teams()
    test_redshift_service_sync()
    print("✅ All tests passed successfully!")
