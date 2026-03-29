#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P28 Tool — Mesh socket authoring, socket transform editing, and preview attachment.
class MeshSocketEditorTool : public ITool {
public:
    enum class SocketType { Bone, Root, Attachment, Projectile, Effect, Audio, Custom };
    enum class SocketSpace { BoneLocal, ComponentLocal, World, Custom };
    enum class PreviewMode { Static, Animated, Physical, Custom };
    enum class SocketVisibility { Always, Selected, EditorOnly, Never, Custom };

    struct SocketDef {
        std::string socketId;
        std::string socketName;
        std::string meshId;
        SocketType socketType{SocketType::Attachment};
        std::string parentBoneName;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotYaw{0.0f};
        float rotPitch{0.0f};
        float rotRoll{0.0f};
        float scaleX{1.0f};
        float scaleY{1.0f};
        float scaleZ{1.0f};
        SocketSpace space{SocketSpace::BoneLocal};
        SocketVisibility visibility{SocketVisibility::EditorOnly};
        bool enabled{true};
    };

    struct PreviewAttachmentDef {
        std::string attachId;
        std::string socketId;
        std::string previewMeshId;
        PreviewMode previewMode{PreviewMode::Static};
        float previewScale{1.0f};
        bool inheritRotation{true};
        bool inheritScale{false};
        bool enabled{true};
    };

    struct SocketConstraintDef {
        std::string constraintId;
        std::string socketId;
        std::string targetSocketId;
        float maxDistance{100.0f};
        float maxAngle{90.0f};
        bool softConstraint{true};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MeshSocketEditorTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateSocket(const SocketDef& def);
    bool DeleteSocket(const std::string& socketId);
    bool EnableSocket(const std::string& socketId, bool enabled);
    bool SetSocketType(const std::string& socketId, SocketType type);
    bool MoveSocket(const std::string& socketId, float x, float y, float z);
    bool RotateSocket(const std::string& socketId, float yaw, float pitch, float roll);
    const SocketDef* GetSocket(const std::string& socketId) const;
    std::vector<std::string> GetAllSocketIds() const;
    std::vector<std::string> GetSocketsByMesh(const std::string& meshId) const;
    std::vector<std::string> GetSocketsByType(SocketType type) const;
    std::vector<std::string> GetSocketsByBone(const std::string& boneName) const;
    std::vector<std::string> GetEnabledSockets() const;
    bool AddPreviewAttachment(const std::string& socketId, const PreviewAttachmentDef& def);
    bool RemovePreviewAttachment(const std::string& attachId);
    bool EnablePreviewAttachment(const std::string& attachId, bool enabled);
    const PreviewAttachmentDef* GetPreviewAttachment(const std::string& attachId) const;
    std::vector<std::string> GetAttachmentsBySocket(const std::string& socketId) const;
    std::vector<std::string> GetAttachmentsByMode(PreviewMode mode) const;
    bool AddConstraint(const std::string& socketId, const SocketConstraintDef& def);
    bool RemoveConstraint(const std::string& constraintId);
    const SocketConstraintDef* GetConstraint(const std::string& constraintId) const;
    std::vector<std::string> GetConstraintsBySocket(const std::string& socketId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, SocketDef> m_sockets;
    std::unordered_map<std::string, PreviewAttachmentDef> m_attachments;
    std::unordered_map<std::string, SocketConstraintDef> m_constraints;
};

} // namespace Atlas::Editor
