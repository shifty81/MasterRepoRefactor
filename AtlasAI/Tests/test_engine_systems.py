"""Tests for G1 (Physics), G2 (AudioSystem), G3 (NetSession), G4 (ScriptingVM)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# G1 — Physics (PhysicsExtensions layer-manager)
# =============================================================================

class TestPhysicsExtensionsFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_physics_types_header(self):
        self._check("Atlas/Engine/Physics/PhysicsTypes.h")

    def test_physics_extensions_header(self):
        self._check("Atlas/Engine/Physics/PhysicsExtensions.h")

    def test_physics_extensions_source(self):
        self._check("Atlas/Engine/Physics/PhysicsExtensions.cpp")


class TestPhysicsTypesContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Physics/PhysicsTypes.h").read_text(encoding="utf-8")

    def test_has_collision_layer_typedef(self):
        self.assertIn("CollisionLayer", self._read())

    def test_has_layers_namespace(self):
        self.assertIn("Layers", self._read())

    def test_world_layer_constant(self):
        self.assertIn("World", self._read())

    def test_dynamic_entity_layer(self):
        self.assertIn("DynamicEntity", self._read())

    def test_trigger_layer(self):
        self.assertIn("Trigger", self._read())

    def test_projectile_layer(self):
        self.assertIn("Projectile", self._read())

    def test_character_layer(self):
        self.assertIn("Character", self._read())

    def test_voxel_chunk_layer(self):
        self.assertIn("VoxelChunk", self._read())

    def test_module_layer(self):
        self.assertIn("Module", self._read())

    def test_editor_only_layer(self):
        self.assertIn("EditorOnly", self._read())

    def test_all_layer_constant(self):
        self.assertIn("All", self._read())

    def test_ephysics_shape_enum(self):
        self.assertIn("EPhysicsShape", self._read())

    def test_ebody_motion_enum(self):
        self.assertIn("EBodyMotion", self._read())

    def test_physics_body_desc(self):
        self.assertIn("PhysicsBodyDesc", self._read())

    def test_physics_body_state(self):
        self.assertIn("PhysicsBodyState", self._read())

    def test_raycast_struct(self):
        self.assertIn("RayCast", self._read())

    def test_raycast_hit_struct(self):
        self.assertIn("RayCastHit", self._read())

    def test_collision_contact(self):
        self.assertIn("CollisionContact", self._read())

    def test_shape_types(self):
        text = self._read()
        for s in ["Box", "Sphere", "Capsule", "ConvexHull", "TriangleMesh"]:
            self.assertIn(s, text, f"Missing shape: {s}")

    def test_motion_types(self):
        text = self._read()
        for m in ["Static", "Kinematic", "Dynamic"]:
            self.assertIn(m, text, f"Missing motion: {m}")


class TestPhysicsExtensionsContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Physics/PhysicsExtensions.h").read_text(encoding="utf-8")

    def test_body_layer_entry(self):
        self.assertIn("BodyLayerEntry", self._read())

    def test_raycast_struct(self):
        self.assertIn("RayCast", self._read())

    def test_raycast_hit_struct(self):
        self.assertIn("RayCastHit", self._read())

    def test_contact_event(self):
        self.assertIn("ContactEvent", self._read())

    def test_contact_callback(self):
        self.assertIn("ContactCallback", self._read())

    def test_trigger_callback(self):
        self.assertIn("TriggerCallback", self._read())

    def test_physics_layer_manager_class(self):
        self.assertIn("PhysicsLayerManager", self._read())

    def test_register_body(self):
        self.assertIn("RegisterBody", self._read())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", self._read())

    def test_get_layer(self):
        self.assertIn("GetLayer", self._read())

    def test_get_collides_with(self):
        self.assertIn("GetCollidesWith", self._read())

    def test_is_trigger(self):
        self.assertIn("IsTrigger", self._read())

    def test_should_collide(self):
        self.assertIn("ShouldCollide", self._read())

    def test_raycast_method(self):
        self.assertIn("Raycast", self._read())

    def test_overlap_sphere(self):
        self.assertIn("OverlapSphere", self._read())

    def test_set_contact_callback(self):
        self.assertIn("SetContactCallback", self._read())

    def test_set_trigger_callback(self):
        self.assertIn("SetTriggerCallback", self._read())

    def test_process_contacts(self):
        self.assertIn("ProcessContacts", self._read())


class TestPhysicsExtensionsImpl(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Physics/PhysicsExtensions.cpp").read_text(encoding="utf-8")

    def test_layer_filter_uses_bitwise_and(self):
        self.assertIn("& cwB", self._read())

    def test_raycast_uses_sphere_approximation(self):
        self.assertIn("sqrt", self._read())

    def test_contact_callback_fires(self):
        self.assertIn("m_contactCb", self._read())

    def test_trigger_callback_fires(self):
        self.assertIn("m_triggerCb", self._read())

    def test_overlap_sphere_distance_check(self):
        self.assertIn("rSum", self._read())


class TestEngineCMakeHasPhysicsAndMore(unittest.TestCase):
    def _cmake(self):
        return (REPO_ROOT / "Atlas/Engine/CMakeLists.txt").read_text(encoding="utf-8")

    def test_has_physics_extensions(self):
        self.assertIn("PhysicsExtensions.cpp", self._cmake())

    def test_has_audio_system(self):
        self.assertIn("AudioSystem.cpp", self._cmake())

    def test_has_net_session(self):
        self.assertIn("NetSession.cpp", self._cmake())

    def test_has_scripting_vm(self):
        self.assertIn("ScriptingVM.cpp", self._cmake())

    def test_has_physics_include_dir(self):
        self.assertIn("/Physics", self._cmake())

    def test_has_audio_include_dir(self):
        self.assertIn("/Audio", self._cmake())

    def test_has_networking_include_dir(self):
        self.assertIn("/Networking", self._cmake())

    def test_has_scripting_include_dir(self):
        self.assertIn("/Scripting", self._cmake())


# =============================================================================
# G2 — Audio System
# =============================================================================

class TestAudioSystemFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_audio_system_header(self):
        self._check("Atlas/Engine/Audio/AudioSystem.h")

    def test_audio_system_source(self):
        self._check("Atlas/Engine/Audio/AudioSystem.cpp")


class TestAudioSystemContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Audio/AudioSystem.h").read_text(encoding="utf-8")

    def test_has_eaudio_category_enum(self):
        self.assertIn("EAudioCategory", self._read())

    def test_has_sound_event_def(self):
        self.assertIn("SoundEventDef", self._read())

    def test_has_sound_instance(self):
        self.assertIn("SoundInstance", self._read())

    def test_has_audio_listener(self):
        self.assertIn("AudioListener", self._read())

    def test_has_audio_system_class(self):
        self.assertIn("AudioSystem", self._read())

    def test_has_register_event(self):
        self.assertIn("RegisterEvent", self._read())

    def test_has_has_event(self):
        self.assertIn("HasEvent", self._read())

    def test_has_get_event_def(self):
        self.assertIn("GetEventDef", self._read())

    def test_has_play_event(self):
        self.assertIn("PlayEvent", self._read())

    def test_has_play_event_3d(self):
        self.assertIn("PlayEvent3D", self._read())

    def test_has_stop_event(self):
        self.assertIn("StopEvent", self._read())

    def test_has_stop_all_in_category(self):
        self.assertIn("StopAllInCategory", self._read())

    def test_has_set_category_volume(self):
        self.assertIn("SetCategoryVolume", self._read())

    def test_has_get_category_volume(self):
        self.assertIn("GetCategoryVolume", self._read())

    def test_has_set_listener(self):
        self.assertIn("SetListener", self._read())

    def test_has_compute_attenuation(self):
        self.assertIn("ComputeAttenuation", self._read())

    def test_has_update_emitter_position(self):
        self.assertIn("UpdateEmitterPosition", self._read())

    def test_has_unregister_emitter(self):
        self.assertIn("UnregisterEmitter", self._read())

    def test_has_playing_count(self):
        self.assertIn("PlayingCount", self._read())

    def test_categories_cover_all(self):
        text = self._read()
        for cat in ["Master", "Music", "SFX", "Voice", "Ambient", "UI"]:
            self.assertIn(cat, text, f"Missing audio category: {cat}")

    def test_has_is_3d_field(self):
        self.assertIn("is3D", self._read())

    def test_has_min_distance_field(self):
        self.assertIn("minDistance", self._read())

    def test_has_max_distance_field(self):
        self.assertIn("maxDistance", self._read())


class TestAudioSystemImpl(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Audio/AudioSystem.cpp").read_text(encoding="utf-8")

    def test_linear_rolloff(self):
        self.assertIn("maxDist - minDist", self._read())

    def test_category_volume_applied_to_existing_instances(self):
        self.assertIn("SetVolume", self._read())

    def test_stopped_instances_pruned(self):
        self.assertIn("Stopped", self._read())


# =============================================================================
# G3 — Network Session
# =============================================================================

class TestNetSessionFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_net_session_header(self):
        self._check("Atlas/Engine/Networking/NetSession.h")

    def test_net_session_source(self):
        self._check("Atlas/Engine/Networking/NetSession.cpp")


class TestNetSessionContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Networking/NetSession.h").read_text(encoding="utf-8")

    def test_has_enet_msg_type_enum(self):
        self.assertIn("ENetMsgType", self._read())

    def test_has_eclient_status_enum(self):
        self.assertIn("EClientStatus", self._read())

    def test_has_client_entry(self):
        self.assertIn("ClientEntry", self._read())

    def test_has_net_message(self):
        self.assertIn("NetMessage", self._read())

    def test_has_net_message_handler(self):
        self.assertIn("NetMessageHandler", self._read())

    def test_has_net_session_class(self):
        self.assertIn("NetSession", self._read())

    def test_has_register_client(self):
        self.assertIn("RegisterClient", self._read())

    def test_has_update_client_status(self):
        self.assertIn("UpdateClientStatus", self._read())

    def test_has_set_client_player_id(self):
        self.assertIn("SetClientPlayerId", self._read())

    def test_has_remove_client(self):
        self.assertIn("RemoveClient", self._read())

    def test_has_find_client(self):
        self.assertIn("FindClient", self._read())

    def test_has_client_count(self):
        self.assertIn("ClientCount", self._read())

    def test_has_get_clients_by_status(self):
        self.assertIn("GetClientsByStatus", self._read())

    def test_has_send(self):
        self.assertIn("void Send", self._read())

    def test_has_broadcast(self):
        self.assertIn("Broadcast", self._read())

    def test_has_broadcast_except(self):
        self.assertIn("BroadcastExcept", self._read())

    def test_has_register_handler(self):
        self.assertIn("RegisterHandler", self._read())

    def test_has_unregister_handler(self):
        self.assertIn("UnregisterHandler", self._read())

    def test_has_dispatch_message(self):
        self.assertIn("DispatchMessage", self._read())

    def test_has_enqueue_received(self):
        self.assertIn("EnqueueReceived", self._read())

    def test_has_process_incoming(self):
        self.assertIn("ProcessIncoming", self._read())

    def test_has_is_server(self):
        self.assertIn("IsServer", self._read())

    def test_has_tick_number(self):
        self.assertIn("TickNumber", self._read())

    def test_has_heartbeat_interval(self):
        self.assertIn("SetHeartbeatIntervalSeconds", self._read())

    def test_msg_types_cover_lifecycle(self):
        text = self._read()
        for t in ["JoinRequest", "JoinAccepted", "JoinRejected",
                  "Disconnect", "Heartbeat"]:
            self.assertIn(t, text, f"Missing msg type: {t}")

    def test_msg_types_cover_world_sync(self):
        text = self._read()
        for t in ["WorldSnapshot", "EntitySpawn", "EntityDestroy", "EntityUpdate"]:
            self.assertIn(t, text, f"Missing sync type: {t}")

    def test_msg_types_cover_economy(self):
        text = self._read()
        for t in ["InventorySync", "TradeOffer", "ContractSync"]:
            self.assertIn(t, text, f"Missing economy msg: {t}")

    def test_client_status_types(self):
        text = self._read()
        for s in ["Connecting", "Authenticated", "InGame", "Disconnected"]:
            self.assertIn(s, text, f"Missing client status: {s}")


# =============================================================================
# G4 — Scripting VM
# =============================================================================

class TestScriptingVMFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_scripting_types_header(self):
        self._check("Atlas/Engine/Scripting/ScriptingTypes.h")

    def test_scripting_vm_header(self):
        self._check("Atlas/Engine/Scripting/ScriptingVM.h")

    def test_scripting_vm_source(self):
        self._check("Atlas/Engine/Scripting/ScriptingVM.cpp")


class TestScriptingTypesContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Scripting/ScriptingTypes.h").read_text(encoding="utf-8")

    def test_has_script_value(self):
        self.assertIn("ScriptValue", self._read())

    def test_has_script_args(self):
        self.assertIn("ScriptArgs", self._read())

    def test_has_script_return(self):
        self.assertIn("ScriptReturn", self._read())

    def test_has_native_function(self):
        self.assertIn("NativeFunction", self._read())

    def test_has_script_binding(self):
        self.assertIn("ScriptBinding", self._read())

    def test_has_script_event(self):
        self.assertIn("ScriptEvent", self._read())

    def test_has_script_event_callback(self):
        self.assertIn("ScriptEventCallback", self._read())

    def test_has_escript_state_enum(self):
        self.assertIn("EScriptState", self._read())

    def test_has_script_context(self):
        self.assertIn("ScriptContext", self._read())

    def test_value_types_cover_all(self):
        text = self._read()
        for t in ["bool", "int64_t", "double", "string", "monostate"]:
            self.assertIn(t, text, f"Missing value type: {t}")

    def test_script_states_defined(self):
        text = self._read()
        for s in ["Idle", "Running", "Suspended", "Error", "Finished"]:
            self.assertIn(s, text, f"Missing script state: {s}")

    def test_has_is_nil(self):
        self.assertIn("IsNil", self._read())

    def test_has_as_bool(self):
        self.assertIn("AsBool", self._read())

    def test_has_as_int(self):
        self.assertIn("AsInt", self._read())

    def test_has_as_float(self):
        self.assertIn("AsFloat", self._read())

    def test_has_as_string(self):
        self.assertIn("AsString", self._read())

    def test_has_module_field(self):
        self.assertIn("module", self._read())

    def test_has_doc_string(self):
        self.assertIn("docString", self._read())


class TestScriptingVMContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Scripting/ScriptingVM.h").read_text(encoding="utf-8")

    def test_has_scripting_vm_class(self):
        self.assertIn("ScriptingVM", self._read())

    def test_has_script_exec_result(self):
        self.assertIn("ScriptExecResult", self._read())

    def test_has_register_binding(self):
        self.assertIn("RegisterBinding", self._read())

    def test_has_unregister_binding(self):
        self.assertIn("UnregisterBinding", self._read())

    def test_has_has_binding(self):
        self.assertIn("HasBinding", self._read())

    def test_has_find_binding(self):
        self.assertIn("FindBinding", self._read())

    def test_has_list_bindings(self):
        self.assertIn("ListBindings", self._read())

    def test_has_create_context(self):
        self.assertIn("CreateContext", self._read())

    def test_has_destroy_context(self):
        self.assertIn("DestroyContext", self._read())

    def test_has_has_context(self):
        self.assertIn("HasContext", self._read())

    def test_has_get_context(self):
        self.assertIn("GetContext", self._read())

    def test_has_list_contexts(self):
        self.assertIn("ListContexts", self._read())

    def test_has_call(self):
        self.assertIn("Call(", self._read())

    def test_has_call_in_context(self):
        self.assertIn("CallInContext", self._read())

    def test_has_subscribe_event(self):
        self.assertIn("SubscribeEvent", self._read())

    def test_has_unsubscribe_event(self):
        self.assertIn("UnsubscribeEvent", self._read())

    def test_has_fire_event(self):
        self.assertIn("FireEvent", self._read())

    def test_has_tick(self):
        self.assertIn("Tick", self._read())

    def test_has_binding_count(self):
        self.assertIn("BindingCount", self._read())

    def test_has_context_count(self):
        self.assertIn("ContextCount", self._read())


class TestScriptingVMImpl(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "Atlas/Engine/Scripting/ScriptingVM.cpp").read_text(encoding="utf-8")

    def test_call_returns_error_on_missing_binding(self):
        self.assertIn("Binding not found", self._read())

    def test_call_checks_min_args(self):
        self.assertIn("Too few arguments", self._read())

    def test_context_state_set_to_running(self):
        self.assertIn("Running", self._read())

    def test_context_state_set_to_error_on_fail(self):
        self.assertIn("Error", self._read())

    def test_fire_event_dispatches_handler(self):
        self.assertIn("m_eventHandlers", self._read())


if __name__ == "__main__":
    unittest.main()
