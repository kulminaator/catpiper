from typing import Callable, Dict

from pipecat.frames.frames import (
    Frame,
    LLMMessagesFrame,
    EndFrame,
    TextFrame, StartFrame,
)
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.task import PipelineTask
from pipecat.pipeline.runner import PipelineRunner
from pipecat.processors.frame_processor import FrameProcessor, FrameDirection
from pipecat.services.ollama import OLLamaLLMService

class LLMRunner:

    async def run_interaction(self, input_message: str, callback: Callable[[str, str], None]):
        # Would be nice to reuse the pipeline, but that is not pipecat's design, #sad.

        # --- Pipeline Setup ---
        # 1. LLM: The OLLama LLM Service component
        llm = OLLamaLLMService(model="llama3")
        # 2. Sink: Our custom sink that executes the callback
        sink = SimpleCallbackSink(callback, input_message)
        # --- Assemble Pipeline ---
        pipeline = Pipeline(processors=[llm, sink])
        task = PipelineTask(pipeline)

        # --- Give it input and run it ---
        await self.enque_request_frames(task, input_message)
        runner = PipelineRunner()
        print(f"🚀 Running pipeline with input message: '{input_message}'...")
        # Run the pipeline until it completes
        await runner.run(task)
        print("✨ Pipeline finished execution.")

    async def enque_request_frames(self, task: PipelineTask,  input_message: str):
        llm_messages: list[Dict[str, str]] = [
            {"role": "system", "content": "You are a friendly, helpful, and concise chatbot. Keep your answers brief."},
            {"role": "user", "content": input_message}
        ]
        await task.queue_frame(LLMMessagesFrame(llm_messages))
        await task.queue_frame(EndFrame())


class SimpleCallbackSink(FrameProcessor):
    def __init__(self, callback: Callable[[str, str], None], input):
        super().__init__()
        self.callback = callback
        self.full_response = ""
        self.input = input

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        # Text response, possibly a part of it
        if isinstance(frame, TextFrame):
            #print(f"Received text frame: {frame.text}")
            self.full_response += frame.text

        # Indicates end of message handling
        elif isinstance(frame, EndFrame):
            self.callback(self.input, self.full_response)
            # cleanly terminate the pipeline
            await self.push_frame(frame)

        elif isinstance(frame, StartFrame):
            #just pass it on, otherwise the pipecat won't start up
            await self.push_frame(frame)
