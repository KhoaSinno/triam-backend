import os
from typing import Any

from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import Agent, AgentServer, AgentSession, RunContext, function_tool, room_io
from livekit.plugins import (
    google,
    noise_cancellation,
    silero,
)
from tavily import TavilyClient

from app.core.config import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

load_dotenv(".env")
if os.getenv("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
if os.getenv("GOOGLE_API_KEY"):
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]


# from app.core.config import settings

# =======SYSTEM INSTRUCTION=======
SYSTEM_INSTRUCTION = """
Bạn là Trợ lý TRIAM - Người hỗ trợ cho người dùng đọc sách qua giọng nói. Bạn có 2 công cụ hỗ trợ:
1. 'search_book_knowledge': Dùng để tìm trong sách của người dùng. Luôn ưu tiên cái này trước.
2. 'search_web': Dùng để tìm thông tin từ Internet nếu sách không có câu trả lời hoặc câu hỏi là về tin tức/kiến thức chung.
Hãy trả lời ngắn gọn, súc tích bằng giọng nói thân thiện.
"""
AGENT_NAME = os.getenv("LIVEKIT_AGENT_NAME", "my-agent").strip()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_INSTRUCTION)

    @function_tool(
        name="search_book_knowledge",
        description="Tra cứu nội dung trong sách hiện tại của người dùng đang đọc. Khi người dùng có các câu hỏi liên quan đến nội dung sách thì hãy sử dụng công cụ này. Ưu tiên tìm trong sách trước khi tìm trên internet.",
    )
    async def search_book_knowledge(
        self,
        context: RunContext,
        query: str,
    ) -> dict[str, Any]:
        """Look up book knowledge for a given query.

        Args:
            query: The query to search for in the book.
        """

        return {
            "book_knowledge": "Rich Dad Poor Dad is written in the style of a set of parables presented as autobiographical.[1] The titular \"rich dad\" is his best friend's father who accumulated wealth due to entrepreneurship and savvy investing, while the \"poor dad\" is claimed to be Kiyosaki's own father who he says worked hard all his life but never obtained financial security. The book advocates the importance of financial literacy, financial independence and building wealth through investing in assets, real estate investing, starting and owning businesses, as well as increasing one's financial intelligence to improve one's business and financial aptitude. It also encourages readers to overcome obstacles to becoming wealthy, including fear, cynicism, laziness, bad habits, and arrogance."
        }

    @function_tool(name="search_web", description="Tra cứu thông tin từ Internet. Chỉ sử dụng công cụ này khi sách không có câu trả lời hoặc kiến thức trong sách không đủ để trả lời câu hỏi.")
    async def search_web(
        self,
        context: RunContext,
        query: str,
    ) -> dict[str, Any]:
        """Look up web knowledge for a given query.

        Args:
            query: The query to search for on the web.
        """

        search_result = await tavily_client.search(
            query=query,
            search_depth="basic",
            max_results=3,
        )
        result_text = "\n".join([f"- {r['content']}" for r in search_result["results"]])

        # Print result_text to console
        print(result_text)

        return {"web_knowledge": result_text}


server = AgentServer()


# Để agent_name rỗng mặc định nhằm auto dispatch (Flutter connect room là agent nhận job).
# Nếu muốn dispatch cứng theo tên, set env LIVEKIT_AGENT_NAME=my-agent.
@server.rtc_session(agent_name=AGENT_NAME)
async def triam_voice_agent(ctx: agents.JobContext):

    session = AgentSession(
        llm=google.realtime.RealtimeModel(
            api_key=os.getenv("GOOGLE_API_KEY"),
            model="models/gemini-2.5-flash-native-audio-latest",
            voice="Puck",
        ),
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Xin chào! Tôi là trợ lý ảo của bạn. Hãy hỏi tôi bất cứ điều gì bạn muốn biết nhé!",
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
