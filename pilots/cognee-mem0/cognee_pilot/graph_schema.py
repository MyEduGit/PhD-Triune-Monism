"""
Node dataclasses and text serialisers for the Cognee knowledge graph.
Each to_text() produces the string Cognee ingests and indexes.
"""
from dataclasses import dataclass


@dataclass
class PhDLayer:
    step_id: str
    step_name: str
    phase_id: int
    phase_name: str
    description: str
    key_finding: str
    deliverables: str
    status: str
    phd_chapter: str
    timeline: str
    governance_principle: str

    def to_text(self) -> str:
        return (
            f"PhD Research Layer — Phase {self.phase_id} ({self.phase_name}), "
            f"Step {self.step_id}: {self.step_name}. "
            f"Description: {self.description}. "
            f"Key Finding: {self.key_finding}. "
            f"Deliverables: {self.deliverables}. "
            f"Status: {self.status}. PhD Chapter: {self.phd_chapter}. "
            f"Timeline: {self.timeline}. "
            f"Governance Principle: {self.governance_principle}."
        )


@dataclass
class AILegislaturePhase:
    phase_id: int
    phase_name: str
    title: str
    description: str
    deliverables: str
    status: str
    infrastructure: str
    dependencies: str
    governance_principle: str
    timeline: str
    agents_involved: str

    def to_text(self) -> str:
        return (
            f"AI Legislature Phase {self.phase_id} ({self.phase_name}): {self.title}. "
            f"Description: {self.description}. "
            f"Deliverables: {self.deliverables}. "
            f"Status: {self.status}. Infrastructure: {self.infrastructure}. "
            f"Depends on: {self.dependencies}. "
            f"Governance Principle: {self.governance_principle}. "
            f"Timeline: {self.timeline}. Agents: {self.agents_involved}."
        )


@dataclass
class CommunityTier:
    tier_id: int
    tier_name: str
    role: str
    description: str
    members_estimate: str
    access_level: str
    infrastructure: str
    revenue_model: str
    current_status: str
    urantios_relation: str
    deliverables_served: str

    def to_text(self) -> str:
        return (
            f"Community/Business Tier {self.tier_id} ({self.tier_name}): {self.role}. "
            f"Description: {self.description}. "
            f"Members: {self.members_estimate}. Access: {self.access_level}. "
            f"Infrastructure: {self.infrastructure}. "
            f"Revenue Model: {self.revenue_model}. "
            f"Status: {self.current_status}. "
            f"UrantiOS Relation: {self.urantios_relation}. "
            f"Serves: {self.deliverables_served}."
        )
