import requests

BASE_URL = "http://mooninsurance.local"

def test_agent_service():
    print("🔍 Testing Agent Service...")
    response = requests.get(f"{BASE_URL}/agent")
    assert response.status_code == 200, "❌ Agent Service failed"
    print("✅ Agent Service passed!")

def test_integration_service():
    print("🔍 Testing Integration Service...")
    response = requests.get(f"{BASE_URL}/sales")
    assert response.status_code == 200, "❌ Integration Service failed"
    print("✅ Integration Service passed!")

def test_notification_service():
    print("🔍 Testing Notification Service...")
    response = requests.get(f"{BASE_URL}/notification/check_target?target=1")
    assert response.status_code == 200, "❌ Notification Service failed"
    print("✅ Notification Service passed!")

def test_aggregator_service_best_teams():
    print("🔍 Testing Aggregator Service (Best Teams)...")
    response = requests.get(f"{BASE_URL}/aggregation/best_teams")
    assert response.status_code == 200, "❌ Aggregator Service failed"
    print("✅ Aggregator Service passed!")

def test_redshift_service_sync():
    print("🔍 Testing Redshift Analytics Service...")
    response = requests.post(f"{BASE_URL}/sync/appointments_per_doctor")
    assert response.status_code == 200, "❌ Redshift Analytics Service failed"
    print("✅ Redshift Analytics Service passed!")

if __name__ == "__main__":
    try:
        test_agent_service()
        test_integration_service()
        test_notification_service()
        test_aggregator_service_best_teams()
        test_redshift_service_sync()
        print("🎉✅ All tests passed successfully!")
    except AssertionError as e:
        print(str(e))
        print("❌ Some tests failed!")
        exit(1)
