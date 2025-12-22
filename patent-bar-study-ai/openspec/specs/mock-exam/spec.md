# Mock Exam Specification

## Purpose

Provide full-length practice examinations that simulate the actual USPTO Patent Bar exam experience, with realistic timing, question distribution, and performance analysis.

## Requirements

### Requirement: Exam Configuration

The system SHALL allow configuration of mock exam parameters.

#### Scenario: Create standard mock exam

- **WHEN** a user starts a standard mock exam
- **THEN** the exam contains 100 questions
- **AND** the time limit is 3 hours (180 minutes)
- **AND** questions are distributed across topics per exam weighting
- **AND** questions are selected to avoid recent repeats

#### Scenario: Create custom mock exam

- **WHEN** a user configures a custom exam
- **THEN** they can set:
  - Question count (25, 50, 75, or 100)
  - Time limit (proportional or custom)
  - Topic focus (specific chapters or topics)
  - Difficulty level (mixed, hard only, etc.)

#### Scenario: Create morning/afternoon split

- **WHEN** a user wants to simulate the actual exam format
- **THEN** the system offers:
  - Morning session (50 questions, 90 minutes)
  - Afternoon session (50 questions, 90 minutes)
  - Full exam (100 questions, 180 minutes with optional break)

### Requirement: Exam Experience

The system SHALL provide a realistic exam simulation experience.

#### Scenario: Display exam interface

- **WHEN** a mock exam is in progress
- **THEN** the interface shows:
  - Current question number and total
  - Remaining time (countdown)
  - Question navigation panel
  - Mark for review toggle
  - Answer selection area

#### Scenario: Navigate between questions

- **WHEN** navigating during an exam
- **THEN** users can:
  - Go to next/previous question
  - Jump to any question by number
  - See which questions are answered, unanswered, or marked
- **AND** navigation does not submit the exam

#### Scenario: Mark questions for review

- **WHEN** a user marks a question for review
- **THEN** a visual indicator shows the mark
- **AND** marked questions are listed in the navigation panel
- **AND** users can filter to show only marked questions

#### Scenario: Handle time expiration

- **WHEN** the time limit expires
- **THEN** the system auto-submits the exam
- **AND** a warning is shown at 30, 10, and 5 minutes remaining
- **AND** unanswered questions are counted as incorrect

### Requirement: Exam Rules Enforcement

The system SHALL enforce exam-like conditions.

#### Scenario: Prevent answer changes after submission

- **WHEN** the exam is submitted
- **THEN** no further answer changes are allowed
- **AND** the submission is final
- **AND** a confirmation is required before submission

#### Scenario: Track time per question

- **WHEN** questions are answered
- **THEN** time spent on each question is recorded
- **AND** this data is available in the post-exam analysis
- **AND** excessive time on questions is flagged

#### Scenario: Handle exam interruption

- **WHEN** the exam is interrupted (browser close, disconnect)
- **THEN** the exam state is preserved
- **AND** the timer continues running
- **AND** the user can resume where they left off
- **AND** interruption is logged in exam records

#### Scenario: Prevent external reference (optional)

- **WHEN** strict mode is enabled
- **THEN** MPEP reference is disabled during exam
- **AND** other study features are inaccessible
- **AND** leaving the exam window triggers a warning

### Requirement: Exam Scoring

The system SHALL provide accurate and detailed scoring.

#### Scenario: Calculate final score

- **WHEN** an exam is completed
- **THEN** the system calculates:
  - Raw score (correct / total)
  - Percentage score
  - Pass/fail status (passing is typically 70%)
  - Score relative to passing threshold

#### Scenario: Score by topic

- **WHEN** reviewing exam results
- **THEN** the system shows performance by:
  - MPEP chapter (e.g., "Chapter 2100: 8/10")
  - Topic area (e.g., "Obviousness: 90%")
  - Question type
  - Difficulty level

#### Scenario: Calculate scaled score (optional)

- **WHEN** historical data is available
- **THEN** the system can estimate a scaled score
- **AND** explains the scaling methodology
- **AND** indicates confidence in the estimate

### Requirement: Exam Review

The system SHALL provide comprehensive post-exam review.

#### Scenario: Review all questions

- **WHEN** a user reviews a completed exam
- **THEN** all questions are accessible with:
  - The user's answer
  - The correct answer
  - Full explanation
  - MPEP reference
  - Time spent on the question

#### Scenario: Filter review by result

- **WHEN** filtering exam review
- **THEN** users can view:
  - All questions
  - Incorrect only
  - Correct only
  - Marked for review
  - By topic or chapter

#### Scenario: Identify patterns in errors

- **WHEN** reviewing incorrect answers
- **THEN** the system identifies:
  - Topics with multiple errors
  - Question types frequently missed
  - Common error patterns
  - Similar questions for additional practice

### Requirement: Exam History

The system SHALL maintain complete exam history.

#### Scenario: View exam history

- **WHEN** a user views their exam history
- **THEN** all completed exams are listed with:
  - Date and time
  - Score and pass/fail status
  - Duration
  - Exam configuration

#### Scenario: Compare exam performance

- **WHEN** comparing exams over time
- **THEN** the system shows:
  - Score trend chart
  - Best/worst performances
  - Topic improvement areas
  - Time management trends

#### Scenario: Retake exam

- **WHEN** a user wants to retake an exam
- **THEN** they can retake with the same questions
- **AND** performance is compared to previous attempts
- **AND** retakes are flagged in history

### Requirement: Exam Analytics

The system SHALL provide detailed exam analytics.

#### Scenario: Time analysis

- **WHEN** reviewing time data
- **THEN** the system shows:
  - Total time used vs. available
  - Average time per question
  - Slowest/fastest questions
  - Time distribution by topic

#### Scenario: Difficulty analysis

- **WHEN** analyzing difficulty
- **THEN** the system shows:
  - Performance by difficulty level
  - Questions where difficulty didn't match user performance
  - Suggested difficulty adjustments for future study

#### Scenario: Readiness assessment

- **WHEN** sufficient exam data exists
- **THEN** the system provides:
  - Predicted actual exam score range
  - Confidence level in prediction
  - Specific recommendations for improvement
  - Suggested exam date readiness

### Requirement: Exam Question Pool

The system SHALL maintain a quality exam question pool.

#### Scenario: Ensure unique exams

- **WHEN** generating an exam
- **THEN** questions are selected to minimize overlap with recent exams
- **AND** at least 80% of questions should be unseen in last 5 exams
- **AND** the system tracks question exposure

#### Scenario: Balance question distribution

- **WHEN** selecting questions
- **THEN** the distribution approximates actual exam weighting:
  - Patentability: ~25%
  - Prosecution Procedures: ~20%
  - Claims: ~15%
  - Post-Grant: ~10%
  - PCT/Foreign: ~10%
  - Formalities: ~10%
  - Appeals: ~5%
  - Ethics: ~5%

#### Scenario: Include various question types

- **WHEN** assembling an exam
- **THEN** questions include:
  - Direct recall questions
  - Scenario/fact pattern questions
  - Calculation questions (fees, dates)
  - Exhibit-based questions (claims, specifications)

### Requirement: Exam Scheduling

The system SHALL help users schedule and prepare for mock exams.

#### Scenario: Schedule mock exam

- **WHEN** a user schedules an exam
- **THEN** a reminder is set for the scheduled time
- **AND** the exam is reserved (questions selected in advance)
- **AND** calendar integration is available

#### Scenario: Recommend exam frequency

- **WHEN** providing study recommendations
- **THEN** the system suggests:
  - Taking a mock exam every 1-2 weeks
  - Increasing frequency as exam date approaches
  - Spacing exams to allow for focused study between

#### Scenario: Pre-exam preparation checklist

- **WHEN** starting a scheduled exam
- **THEN** the system shows a checklist:
  - 3-hour block of uninterrupted time
  - Quiet environment
  - No reference materials (if simulating real conditions)
  - Scratch paper ready (physical or digital)

### Requirement: Accessibility

The system SHALL ensure exam accessibility.

#### Scenario: Extended time accommodation

- **WHEN** a user needs extended time
- **THEN** time limits can be adjusted (1.5x, 2x)
- **AND** this is reflected in analytics
- **AND** time extension is noted in exam records

#### Scenario: Pause exam (non-timed mode)

- **WHEN** taking an untimed practice exam
- **THEN** the exam can be paused and resumed
- **AND** total active time is still tracked
- **AND** the user can take breaks as needed
