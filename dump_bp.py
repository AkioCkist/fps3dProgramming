import unreal

def P(*a):
    unreal.log(" ".join(str(x) for x in a))

# Slot node names via multiple accessors
abp = unreal.load_asset("/Game/InfimaGames/FreeFPSTemplate/Core/ABP_Character")
nodes = abp.get_nodes_of_class(unreal.AnimGraphNode_Slot)
for n in nodes:
    val = None
    how = "?"
    for accessor in [
        lambda: n.get_editor_property("slot_name"),
        lambda: n.slot_name,
        lambda: n.get_editor_property("SlotName"),
    ]:
        try:
            val = accessor()
            how = accessor.__name__ if hasattr(accessor, "__name__") else "?"
            break
        except Exception as e:
            last = e
    P("SLOTNODE", n.get_name(), "->", val)

# Cached pose names
for n in abp.get_nodes_of_class(unreal.AnimGraphNode_SaveCachedPose):
    try:
        P("SAVE", n.get_name(), "cache=", n.get_editor_property("cache_pose_name"))
    except Exception as e:
        P("SAVE", n.get_name(), "ERR", e)
for n in abp.get_nodes_of_class(unreal.AnimGraphNode_UseCachedPose):
    try:
        P("USE", n.get_name(), "cache=", n.get_editor_property("cache_pose_name"))
    except Exception as e:
        P("USE", n.get_name(), "ERR", e)

# Runtime montage test
P("=" * 60)
P("RUNTIME MONTAGE TEST")
try:
    edsub = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = edsub.get_editor_world()
    cls = unreal.load_asset("/Game/InfimaGames/FreeFPSTemplate/Core/BP_Character.BP_Character_C")
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, unreal.Vector(0, 0, 100), unreal.Rotator(0, 0, 0))
    P("spawned:", actor.get_name() if actor else None)
    arms = None
    for c in actor.get_components_by_class(unreal.SkeletalMeshComponent):
        if c.get_name() == "CharacterArms":
            arms = c
    P("arms:", arms)
    ai = arms.get_anim_instance()
    P("anim instance:", ai.get_class().get_name() if ai else None)

    montage = unreal.load_asset("/Game/InfimaGames/FreeFPSTemplate/Art/AssaultRifle/Animations/AM_FP_AssaultRifle_Fire")
    P("montage:", montage)
    result = ai.montage_play(montage)
    P("montage_play return:", result)
    P("montage_is_active:", ai.montage_is_active(montage))
    try:
        P("is_any_montage_playing:", ai.is_any_montage_playing())
    except Exception as e:
        P("is_any err", e)
    try:
        w = ai.blueprint_get_slot_montage_local_weight("DefaultSlot")
        P("DefaultSlot weight:", w)
    except Exception as e:
        P("weight err", e)
    # stop after test
    ai.montage_stop(0.0)
except Exception as e:
    P("RUNTIME ERR:", e)

P("DONE")
