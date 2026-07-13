package com.example.auth.entity;
import com.fasterxml.uuid.Generators;
import org.hibernate.engine.spi.SharedSessionContractImplementor;
import org.hibernate.id.IdentifierGenerator;
import java.io.Serializable;


public class UuidV7Generator implements IdentifierGenerator {
    @Override
    public Serializable generate(SharedSessionContractImplementor session, Object object) {
        // Sinh ra chuỗi UUIDv7 dựa trên thời gian thực tế
        return Generators.timeBasedEpochGenerator().generate();
    }
} 