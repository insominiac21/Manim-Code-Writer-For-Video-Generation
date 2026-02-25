# MentorBoxAI: Requirements Documentation

---

## 🌟 Introduction

MentorBoxAI is an AI-powered learning assistant that transforms complex technical and educational concepts into cinematic 3Blue1Brown-style animated explainers. Designed for the **Student Track: AI for Learning & Developer Productivity** challenge, the platform helps people learn faster and work smarter by automatically generating visual content from simple text prompts.

---

## 🎯 Problem Statement Alignment

**Target Problem:** Build an AI-powered solution that helps people learn faster, work smarter, or become more productive while building or understanding technology.

**Our Solution:** MentorBoxAI serves as a learning assistant and explainer that:
- Simplifies complex concepts through automated visual storytelling
- Accelerates learning by converting text into 60-second animated explainers
- Improves productivity by eliminating the need for manual animation creation
- Enhances understanding through cinematic mathematical and scientific visualizations

---

## 🧩 Focus Areas Addressed

✅ Clarity: Self-healing AI pipeline ensures crash-proof, reliable visual explanations  
✅ Usefulness: Transforms any topic into professional educational content instantly  
✅ Meaningful AI Impact: 6-layer pipeline meaningfully improves learning experience through automated visual generation

---

## 📚 Glossary

- **System**: The MentorBoxAI learning assistant platform
- **User**: Students, developers, educators, or anyone seeking to understand complex concepts
- **Topic_Prompt**: Natural language input describing any concept to be explained visually
- **Learning_Assistant**: AI-powered system that converts concepts into visual explanations
- **Animation_Pipeline**: The 6-layer AI processing system that converts prompts to educational videos
- **Manim_Code**: Python code using Manim Community Edition for animation generation
- **Self_Healing**: Automatic error detection and correction mechanism ensuring reliability
- **Render_Job**: A video generation task with tracking and status updates
- **Educational_Video**: Final 60-second animated explainer output optimized for learning
- **Technical_Constraints**: System limitations for screen bounds, object limits, and text lengths
- **Concept_Simplification**: AI process that breaks down complex topics into digestible visual components

---

## 📝 Functional & Technical Requirements

### Functional Requirement 1: AI-Powered Learning Acceleration

**User Story:** As a learner (student, developer, or professional), I want to input any complex concept and receive an instant visual explanation, so that I can understand difficult topics faster without spending hours creating or searching for educational content.

#### Acceptance Criteria

1. WHEN a user submits any topic prompt (technical or non-technical), THE System SHALL process it through the 6-layer AI pipeline
2. WHEN processing is complete, THE System SHALL generate a 60-second educational video that simplifies complex concepts through visual storytelling
3. WHEN the topic is technical, THE System SHALL break down complex workflows, algorithms, or systems into digestible visual components
4. THE System SHALL complete video generation within 60 seconds excluding render time, enabling rapid learning iteration
5. WHEN generating content, THE System SHALL focus on clarity and conceptual understanding over memorization
6. THE System SHALL render videos in multiple quality levels (480p-4K) for different learning contexts

---

### Functional Requirement 2: Self-Healing Reliability for Productivity

**User Story:** As a busy learner or developer, I want the system to work reliably without technical failures, so that I can focus on learning rather than troubleshooting AI-generated content.

#### Acceptance Criteria

1. WHEN the AI generates Manim code with errors, THE System SHALL automatically detect and correct them without user intervention
2. WHEN code validation fails, THE System SHALL apply error fixes and re-validate until successful, ensuring 100% success rate
3. THE System SHALL achieve zero runtime crashes through self-healing architecture, maximizing learning productivity
4. WHEN LaTeX rendering would cause crashes, THE System SHALL use zero-LaTeX architecture alternatives
5. THE System SHALL validate all generated code against technical constraints before execution
6. THE System SHALL implement few-shot prompting with golden examples from `few_shot_examples.py` to ensure consistent quality

---

### Functional Requirement 3: Concept Simplification and Clarity

**User Story:** As someone trying to understand complex topics, I want the system to present information in a clear, structured way that doesn't overwhelm me, so that I can build understanding progressively.

#### Acceptance Criteria

1. WHEN generating titles, THE System SHALL limit them to maximum 25 characters for clarity and focus
2. WHEN creating captions, THE System SHALL limit each line to maximum 50 characters for readability
3. WHEN positioning objects, THE System SHALL keep x coordinates between -6 and 6 for optimal viewing
4. WHEN positioning objects, THE System SHALL keep y coordinates between -3.5 and 3.5 for screen compatibility
5. WHEN creating scenes, THE System SHALL limit to maximum 3 objects per scene to avoid cognitive overload
6. THE System SHALL generate information-dense scenes (2-3 labeled objects per scene) that maximize learning efficiency

---

### Functional Requirement 4: AI-Enhanced Content Generation Pipeline

**User Story:** As an educator or content creator, I want the system to intelligently structure explanations with proper pacing and visual flow, so that the generated content is pedagogically sound and engaging.

#### Acceptance Criteria

1. WHEN processing begins, THE Understanding_Layer SHALL analyze the topic and identify key learning objectives and concepts
2. WHEN the script is ready, THE Storyboarding_Layer SHALL plan scene-by-scene visuals optimized for comprehension and retention
3. WHEN storyboarding completes, THE Verification_Layer SHALL validate against both technical constraints and learning effectiveness
4. WHEN verification passes, THE Code_Generation_Layer SHALL produce Manim Python code using proven educational visualization patterns
5. WHEN code is generated, THE Refinement_Layer SHALL enhance visual quality with effects that support rather than distract from learning
6. WHEN refinement completes, THE Validation_Layer SHALL ensure the final output meets both technical and pedagogical standards
7. THE System SHALL implement topic-specific visual patterns (mathematics, programming, science, business) optimized for different learning domains

---

### Functional Requirement 5: Developer-Friendly Learning Interface

**User Story:** As a developer or technical professional, I want an intuitive interface that lets me quickly generate explanations for complex systems, APIs, or algorithms, so that I can improve my productivity when learning or teaching technical concepts.

#### Acceptance Criteria

1. WHEN a user accesses the platform, THE System SHALL display a developer-friendly web dashboard using `frontend/index.html`
2. WHEN a user submits a topic, THE System SHALL create a tracked render job with detailed progress indicators for transparency
3. WHEN generation is in progress, THE System SHALL display real-time progress indicators via `frontend/app.js` showing which AI layer is processing
4. WHEN a video is complete, THE System SHALL provide immediate preview and download options for rapid iteration
5. WHEN multiple jobs exist, THE System SHALL display a job history with status for each request, supporting batch learning workflows
6. THE System SHALL provide duration and quality controls for different use cases (quick preview vs. presentation-ready)

---

### Functional Requirement 6: Knowledge Organization and Skill Building

**User Story:** As a learner building expertise in a domain, I want the system to create content that builds on foundational concepts and includes practical insights, so that I can develop deep understanding rather than surface-level knowledge.

#### Acceptance Criteria

1. WHEN generating educational content, THE System SHALL include key principles, relationships, and practical applications relevant to the topic
2. WHEN creating visuals, THE System SHALL use progressive disclosure and visual hierarchy to support skill building
3. WHEN presenting information, THE System SHALL structure content for optimal 60-second learning sessions with clear takeaways
4. THE System SHALL generate all visuals procedurally without requiring external assets, ensuring consistent availability
5. WHEN covering technical topics, THE System SHALL ensure accuracy and include real-world context for practical application
6. THE System SHALL provide actionable insights and next steps in every video to support continuous learning

---

### Technical Requirement 7: Scalable Learning Infrastructure

**User Story:** As an organization or educational institution, I want robust backend services that can handle multiple concurrent learners, so that the platform can scale to support team learning and organizational knowledge sharing.

#### Acceptance Criteria

1. THE System SHALL provide FastAPI-based REST endpoints for video generation requests via `src/app/api/v1/endpoints.py`
2. WHEN receiving requests, THE System SHALL integrate with AWS Bedrock Claude 3 Sonnet for advanced reasoning
3. WHEN processing videos, THE System SHALL use Manim Community Edition for professional-quality animation rendering
4. WHEN rendering output, THE System SHALL use FFmpeg, Cairo, and Pango for optimized video production
5. THE System SHALL handle concurrent requests and maintain job queue management for organizational scalability
6. THE System SHALL be configurable for different LLM backends to support various organizational needs

---

### Technical Requirement 8: Learning-Optimized Error Handling

**User Story:** As a learner using the system for important study or work sessions, I want clear feedback when issues occur and automatic recovery, so that technical problems don't interrupt my learning flow.

#### Acceptance Criteria

1. WHEN API errors occur, THE System SHALL return descriptive error messages with suggested learning alternatives
2. WHEN AI model failures happen, THE System SHALL implement retry mechanisms with exponential backoff while keeping users informed
3. WHEN rendering fails, THE System SHALL log detailed error information and provide simplified fallback explanations
4. WHEN system resources are unavailable, THE System SHALL queue requests and provide estimated wait times to support learning planning
5. THE System SHALL support horizontal scaling capability to serve learning communities of any size

---

## 📚 Further Reading
- See UPDATED_ARCHITECTURE.md for system architecture and data flow.
- See DESIGN.md for design principles and component map.
